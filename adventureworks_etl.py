"""
Advanced ETL Pipeline for AdventureWorks Dataset
Includes data cleansing, preprocessing, and comprehensive KPI generation
for multi-agent MCP Business Intelligence Dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import warnings
warnings.filterwarnings('ignore')

class DataCleansing:
    """Advanced data cleansing and preprocessing module"""
    
    @staticmethod
    def handle_missing_values(df, numeric_strategy='median', categorical_strategy='mode'):
        """Handle missing values with smart strategies"""
        print(f"  - Handling missing values...")
        initial_nulls = df.isnull().sum().sum()
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                if numeric_strategy == 'median':
                    df[col].fillna(df[col].median(), inplace=True)
                elif numeric_strategy == 'mean':
                    df[col].fillna(df[col].mean(), inplace=True)
                else:
                    df[col].fillna(0, inplace=True)
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                if categorical_strategy == 'mode' and not df[col].mode().empty:
                    df[col].fillna(df[col].mode()[0], inplace=True)
                else:
                    df[col].fillna('Unknown', inplace=True)
        
        final_nulls = df.isnull().sum().sum()
        print(f"    ✓ Filled {initial_nulls - final_nulls} missing values")
        return df
    
    @staticmethod
    def remove_duplicates(df, subset=None):
        """Remove duplicate records"""
        initial_count = len(df)
        df.drop_duplicates(subset=subset, keep='first', inplace=True)
        removed = initial_count - len(df)
        if removed > 0:
            print(f"    ✓ Removed {removed} duplicate records")
        return df
    
    @staticmethod
    def detect_outliers(df, columns, method='iqr', action='cap'):
        """Detect and handle outliers using IQR method"""
        print(f"  - Detecting outliers in {len(columns)} columns...")
        outliers_count = 0
        
        for col in columns:
            if col in df.columns and df[col].dtype in [np.float64, np.int64]:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                outliers_count += outliers
                
                if action == 'cap' and outliers > 0:
                    df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
                elif action == 'remove' and outliers > 0:
                    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        if outliers_count > 0:
            print(f"    ✓ Handled {outliers_count} outliers")
        return df
    
    @staticmethod
    def standardize_text(df, columns):
        """Standardize text fields"""
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.title()
        return df
    
    @staticmethod
    def validate_and_parse_dates(df, date_columns):
        """Validate and parse date columns"""
        print(f"  - Parsing date columns...")
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    invalid_dates = df[col].isnull().sum()
                    if invalid_dates > 0:
                        print(f"    ⚠ {invalid_dates} invalid dates in {col}")
                except Exception as e:
                    print(f"    ⚠ Error parsing {col}: {str(e)}")
        return df


class AdvancedKPICalculator:
    """Calculate advanced business KPIs"""
    
    @staticmethod
    def calculate_rfm_score(sales_df, current_date=None):
        """Calculate RFM (Recency, Frequency, Monetary) customer segmentation"""
        if current_date is None:
            current_date = sales_df['OrderDate'].max()
        
        rfm = sales_df.groupby('CustomerID').agg({
            'OrderDate': lambda x: (current_date - x.max()).days,
            'SalesOrderID': 'nunique',
            'SubTotal': 'sum'
        }).reset_index()
        
        rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
        
        # Score each dimension (1-5)
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')
        
        rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
        
        # Segment customers
        rfm['Segment'] = 'Regular'
        rfm.loc[rfm['RFM_Score'].str[:2].astype(int) >= 44, 'Segment'] = 'Champions'
        rfm.loc[rfm['RFM_Score'].str[:2].astype(int) <= 22, 'Segment'] = 'At Risk'
        
        return rfm
    
    @staticmethod
    def calculate_customer_lifetime_value(sales_df):
        """Calculate Customer Lifetime Value"""
        customer_metrics = sales_df.groupby('CustomerID').agg({
            'SubTotal': 'sum',
            'SalesOrderID': 'nunique',
            'OrderDate': lambda x: (x.max() - x.min()).days
        }).reset_index()
        
        customer_metrics.columns = ['CustomerID', 'TotalRevenue', 'OrderCount', 'CustomerLifespanDays']
        customer_metrics['AvgOrderValue'] = customer_metrics['TotalRevenue'] / customer_metrics['OrderCount']
        customer_metrics['CustomerLifespanDays'] = customer_metrics['CustomerLifespanDays'].replace(0, 1)
        
        # Simple CLV = Avg Order Value * Purchase Frequency * Customer Lifespan (annualized)
        customer_metrics['PurchaseFrequency'] = customer_metrics['OrderCount'] / (customer_metrics['CustomerLifespanDays'] / 365)
        customer_metrics['CLV'] = customer_metrics['AvgOrderValue'] * customer_metrics['PurchaseFrequency'] * 3  # 3-year projection
        
        return customer_metrics['CLV'].mean()
    
    @staticmethod
    def calculate_employee_risk_score(employee_df):
        """Calculate attrition risk score for employees"""
        risk_scores = []
        
        for idx, emp in employee_df.iterrows():
            risk = 0
            
            # Age-based risk
            if 'Age' in employee_df.columns:
                if emp.get('Age', 0) < 25 or emp.get('Age', 0) > 55:
                    risk += 1
            
            # Tenure-based risk
            if 'Tenure_Years' in employee_df.columns:
                if emp.get('Tenure_Years', 0) < 1:
                    risk += 2
                elif emp.get('Tenure_Years', 0) > 10:
                    risk += 1
            
            # Gender diversity (simplified)
            if emp.get('Gender') in ['M', 'F']:
                risk += 0  # Neutral
            
            # Marital status
            if emp.get('MaritalStatus') == 'S':
                risk += 0.5
            
            risk_scores.append(min(risk, 5))  # Cap at 5
        
        return risk_scores


class AdventureWorksETL:
    """Complete ETL Pipeline for AdventureWorks dataset"""
    
    def __init__(self, data_path: str = "./data/raw/"):
        self.data_path = data_path
        self.cleaner = DataCleansing()
        self.kpi_calculator = AdvancedKPICalculator()
        self.sales_data = None
        self.hr_data = None
        self.finance_data = None
        
    def extract(self):
        """Extract data from CSV files"""
        print("\n" + "="*60)
        print("STEP 1: EXTRACTING DATA")
        print("="*60)
        
        try:
            # Sales related tables
            print("Loading sales data...")
            self.sales_orders = pd.read_csv(f"{self.data_path}Sales_SalesOrderHeader.csv", encoding='utf-8', low_memory=False)
            self.sales_details = pd.read_csv(f"{self.data_path}Sales_SalesOrderDetail.csv", encoding='utf-8', low_memory=False)
            self.customers = pd.read_csv(f"{self.data_path}Sales_Customer.csv", encoding='utf-8', low_memory=False)
            
            try:
                self.products = pd.read_csv(f"{self.data_path}Production_Product.csv", encoding='utf-8', low_memory=False)
            except FileNotFoundError:
                print("  ⚠ Products file not found, continuing without it")
                self.products = None
            
            # HR related tables
            print("Loading HR data...")
            self.employees = pd.read_csv(f"{self.data_path}HumanResources_Employee.csv", encoding='utf-8', low_memory=False)
            
            try:
                self.departments = pd.read_csv(f"{self.data_path}HumanResources_Department.csv", encoding='utf-8', low_memory=False)
            except FileNotFoundError:
                print("  ⚠ Departments file not found, continuing without it")
                self.departments = None
            
            print("✓ Data extraction completed successfully")
            print(f"  - Sales Orders: {len(self.sales_orders)} records")
            print(f"  - Sales Details: {len(self.sales_details)} records")
            print(f"  - Customers: {len(self.customers)} records")
            print(f"  - Employees: {len(self.employees)} records")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            print("\nExpected file structure:")
            print("  data/raw/Sales_SalesOrderHeader.csv")
            print("  data/raw/Sales_SalesOrderDetail.csv")
            print("  data/raw/Sales_Customer.csv")
            print("  data/raw/Production_Product.csv (optional)")
            print("  data/raw/HumanResources_Employee.csv")
            print("  data/raw/HumanResources_Department.csv (optional)")
            return False
    
    def clean_and_preprocess(self):
        """Clean and preprocess all datasets"""
        print("\n" + "="*60)
        print("STEP 2: DATA CLEANSING & PREPROCESSING")
        print("="*60)
        
        # Clean sales data
        print("\nCleaning sales orders...")
        self.sales_orders = self.cleaner.validate_and_parse_dates(
            self.sales_orders, ['OrderDate', 'DueDate', 'ShipDate']
        )
        self.sales_orders = self.cleaner.handle_missing_values(self.sales_orders)
        self.sales_orders = self.cleaner.remove_duplicates(self.sales_orders, subset=['SalesOrderID'])
        self.sales_orders = self.cleaner.detect_outliers(
            self.sales_orders, ['SubTotal', 'TaxAmt', 'Freight', 'TotalDue'], action='cap'
        )
        
        print("\nCleaning sales details...")
        self.sales_details = self.cleaner.handle_missing_values(self.sales_details)
        self.sales_details = self.cleaner.remove_duplicates(
            self.sales_details, subset=['SalesOrderID', 'SalesOrderDetailID']
        )
        
        # Clean HR data
        print("\nCleaning employee data...")
        self.employees = self.cleaner.validate_and_parse_dates(
            self.employees, ['BirthDate', 'HireDate']
        )
        self.employees = self.cleaner.handle_missing_values(self.employees)
        self.employees = self.cleaner.remove_duplicates(self.employees, subset=['BusinessEntityID'])
        
        print("\n✓ Data cleansing completed")
    
    def transform_sales_data(self):
        """Transform sales data with advanced KPIs"""
        print("\n" + "="*60)
        print("STEP 3A: TRANSFORMING SALES DATA")
        print("="*60)
        
        # Merge sales orders with details
        sales_full = self.sales_orders.merge(
            self.sales_details, 
            on='SalesOrderID', 
            how='inner'
        )
        
        # Add product information if available
        if self.products is not None:
            sales_full = sales_full.merge(
                self.products[['ProductID', 'Name', 'StandardCost', 'ListPrice']], 
                on='ProductID', 
                how='left'
            )
        
        # Extract time features
        if 'OrderDate' in sales_full.columns:
            sales_full['Year'] = sales_full['OrderDate'].dt.year
            sales_full['Month'] = sales_full['OrderDate'].dt.month
            sales_full['Quarter'] = sales_full['OrderDate'].dt.quarter
            sales_full['DayOfWeek'] = sales_full['OrderDate'].dt.dayofweek
            sales_full['WeekOfYear'] = sales_full['OrderDate'].dt.isocalendar().week
        
        # Calculate basic metrics
        total_revenue = float(sales_full['SubTotal_x'].sum() if 'SubTotal_x' in sales_full.columns else 0)
        total_orders = int(sales_full['SalesOrderID'].nunique())
        total_customers = int(self.customers.shape[0])
        avg_order_value = float(sales_full['SubTotal_x'].mean() if 'SubTotal_x' in sales_full.columns else 0)
        
        # Advanced KPIs
        print("Calculating advanced sales KPIs...")
        
        # Customer Lifetime Value
        clv = 0
        try:
            clv = float(self.kpi_calculator.calculate_customer_lifetime_value(sales_full))
            print(f"  ✓ Customer Lifetime Value: ${clv:,.2f}")
        except Exception as e:
            print(f"  ⚠ CLV calculation skipped: {str(e)}")
        
        # RFM Segmentation
        rfm_segments = {}
        try:
            rfm = self.kpi_calculator.calculate_rfm_score(sales_full)
            rfm_segments = rfm['Segment'].value_counts().to_dict()
            print(f"  ✓ RFM Segmentation completed: {len(rfm)} customers")
        except Exception as e:
            print(f"  ⚠ RFM calculation skipped: {str(e)}")
        
        # Repeat purchase rate
        customer_order_counts = sales_full.groupby('CustomerID')['SalesOrderID'].nunique()
        repeat_customers = (customer_order_counts > 1).sum()
        repeat_purchase_rate = float(repeat_customers / len(customer_order_counts) * 100) if len(customer_order_counts) > 0 else 0
        
        # Sales growth (YoY if multi-year data)
        sales_by_year = {}
        growth_rate = 0
        if 'Year' in sales_full.columns:
            sales_by_year = sales_full.groupby('Year')['SubTotal_x'].sum().to_dict()
            years = sorted(sales_by_year.keys())
            if len(years) >= 2:
                growth_rate = float((sales_by_year[years[-1]] - sales_by_year[years[-2]]) / sales_by_year[years[-2]] * 100)
        
        # Top products
        top_products = []
        if 'Name' in sales_full.columns:
            top_products = sales_full.groupby('Name')['SubTotal_x'].sum().nlargest(10).to_dict()
        
        # Assemble sales data
        self.sales_data = {
            'summary': {
                'total_revenue': round(total_revenue, 2),
                'total_orders': total_orders,
                'total_customers': total_customers,
                'average_order_value': round(avg_order_value, 2),
                'customer_lifetime_value': round(clv, 2),
                'repeat_purchase_rate': round(repeat_purchase_rate, 2),
                'year_over_year_growth': round(growth_rate, 2)
            },
            'rfm_segments': rfm_segments,
            'by_year': sales_full.groupby('Year')['SubTotal_x'].sum().to_dict() if 'Year' in sales_full.columns else {},
            'by_quarter': sales_full.groupby(['Year', 'Quarter'])['SubTotal_x'].sum().to_dict() if 'Quarter' in sales_full.columns else {},
            'by_month': sales_full.groupby(['Year', 'Month'])['SubTotal_x'].sum().to_dict() if 'Month' in sales_full.columns else {},
            'top_products': {str(k): float(v) for k, v in top_products.items()} if top_products else {},
            'insights': [
                f"Total Revenue: ${total_revenue:,.2f}",
                f"Average Order Value: ${avg_order_value:,.2f}",
                f"Repeat Purchase Rate: {repeat_purchase_rate:.1f}%",
                f"Customer Lifetime Value: ${clv:,.2f}",
                f"YoY Growth Rate: {growth_rate:+.1f}%"
            ]
        }
        
        print("✓ Sales data transformation completed")
        return self.sales_data
    
    def transform_hr_data(self):
        """Transform HR data with advanced KPIs"""
        print("\n" + "="*60)
        print("STEP 3B: TRANSFORMING HR DATA")
        print("="*60)
        
        employees_df = self.employees.copy()
        
        # Merge with departments if available
        if self.departments is not None:
            try:
                employees_df = employees_df.merge(
                    self.departments,
                    left_on='DepartmentID' if 'DepartmentID' in employees_df.columns else 'OrganizationNode',
                    right_on='DepartmentID',
                    how='left'
                )
            except Exception as e:
                print(f"  ⚠ Department merge skipped: {str(e)}")
        
        # Calculate derived fields
        if 'HireDate' in employees_df.columns:
            employees_df['Tenure_Years'] = (datetime.now() - employees_df['HireDate']).dt.days / 365.25
        
        if 'BirthDate' in employees_df.columns:
            employees_df['Age'] = (datetime.now() - employees_df['BirthDate']).dt.days / 365.25
        
        # Calculate risk scores
        print("Calculating employee risk scores...")
        try:
            employees_df['RiskScore'] = self.kpi_calculator.calculate_employee_risk_score(employees_df)
            high_risk_employees = (employees_df['RiskScore'] >= 3).sum()
            print(f"  ✓ Risk analysis completed: {high_risk_employees} high-risk employees")
        except Exception as e:
            print(f"  ⚠ Risk calculation skipped: {str(e)}")
            employees_df['RiskScore'] = 0
        
        # Basic metrics
        total_employees = int(employees_df.shape[0])
        avg_tenure = float(employees_df['Tenure_Years'].mean()) if 'Tenure_Years' in employees_df.columns else 0
        avg_age = float(employees_df['Age'].mean()) if 'Age' in employees_df.columns else 0
        total_departments = int(self.departments.shape[0]) if self.departments is not None else 0
        
        # Advanced metrics
        gender_diversity_ratio = 0
        if 'Gender' in employees_df.columns:
            gender_counts = employees_df['Gender'].value_counts()
            if len(gender_counts) >= 2:
                gender_diversity_ratio = float(min(gender_counts) / max(gender_counts) * 100)
        
        high_risk_count = int((employees_df['RiskScore'] >= 3).sum())
        high_risk_percentage = float(high_risk_count / total_employees * 100) if total_employees > 0 else 0
        
        # Department distribution
        dept_distribution = {}
        if 'Name_y' in employees_df.columns:
            dept_distribution = employees_df['Name_y'].value_counts().to_dict()
        elif 'DepartmentID' in employees_df.columns:
            dept_distribution = employees_df['DepartmentID'].value_counts().to_dict()
        
        # Assemble HR data
        self.hr_data = {
            'summary': {
                'total_employees': total_employees,
                'average_tenure_years': round(avg_tenure, 2),
                'average_age': round(avg_age, 1),
                'total_departments': total_departments,
                'gender_diversity_ratio': round(gender_diversity_ratio, 2),
                'high_risk_employees': high_risk_count,
                'high_risk_percentage': round(high_risk_percentage, 2)
            },
            'by_department': {str(k): int(v) for k, v in dept_distribution.items()},
            'by_gender': employees_df['Gender'].value_counts().to_dict() if 'Gender' in employees_df.columns else {},
            'by_marital_status': employees_df['MaritalStatus'].value_counts().to_dict() if 'MaritalStatus' in employees_df.columns else {},
            'tenure_distribution': {
                '0-2 years': int(((employees_df['Tenure_Years'] >= 0) & (employees_df['Tenure_Years'] < 2)).sum() if 'Tenure_Years' in employees_df.columns else 0),
                '2-5 years': int(((employees_df['Tenure_Years'] >= 2) & (employees_df['Tenure_Years'] < 5)).sum() if 'Tenure_Years' in employees_df.columns else 0),
                '5-10 years': int(((employees_df['Tenure_Years'] >= 5) & (employees_df['Tenure_Years'] < 10)).sum() if 'Tenure_Years' in employees_df.columns else 0),
                '10+ years': int((employees_df['Tenure_Years'] >= 10).sum() if 'Tenure_Years' in employees_df.columns else 0)
            },
            'insights': [
                f"Total Employees: {total_employees}",
                f"Average Tenure: {avg_tenure:.1f} years",
                f"Gender Diversity Ratio: {gender_diversity_ratio:.1f}%",
                f"High-Risk Employees: {high_risk_count} ({high_risk_percentage:.1f}%)",
                f"Average Age: {avg_age:.1f} years"
            ],
            'recommendations': self._generate_hr_recommendations(
                high_risk_percentage, avg_tenure, gender_diversity_ratio
            )
        }
        
        print("✓ HR data transformation completed")
        return self.hr_data
    
    def transform_finance_data(self):
        """Transform finance data with advanced KPIs"""
        print("\n" + "="*60)
        print("STEP 3C: TRANSFORMING FINANCE DATA")
        print("="*60)
        
        sales_full = self.sales_orders.copy()
        
        # Parse dates
        if 'OrderDate' in sales_full.columns:
            sales_full['Year'] = sales_full['OrderDate'].dt.year
            sales_full['Month'] = sales_full['OrderDate'].dt.month
            sales_full['Quarter'] = sales_full['OrderDate'].dt.quarter
        
        # Basic financial metrics
        total_revenue = float(sales_full['SubTotal'].sum()) if 'SubTotal' in sales_full.columns else 0
        total_tax = float(sales_full['TaxAmt'].sum()) if 'TaxAmt' in sales_full.columns else 0
        total_freight = float(sales_full['Freight'].sum()) if 'Freight' in sales_full.columns else 0
        total_gross_profit = float(sales_full['TotalDue'].sum()) if 'TotalDue' in sales_full.columns else 0
        
        # Advanced metrics
        gross_margin = float((total_gross_profit - total_revenue) / total_revenue * 100) if total_revenue > 0 else 0
        tax_rate = float(total_tax / total_revenue * 100) if total_revenue > 0 else 0
        
        # Revenue per employee
        revenue_per_employee = float(total_revenue / len(self.employees)) if len(self.employees) > 0 else 0
        
        # Monthly trends
        monthly_revenue = {}
        quarterly_revenue = {}
        if 'Year' in sales_full.columns and 'Month' in sales_full.columns:
            monthly_revenue = sales_full.groupby(['Year', 'Month'])['SubTotal'].sum().to_dict()
            monthly_revenue = {f"{k[0]}-{k[1]:02d}": float(v) for k, v in monthly_revenue.items()}
        
        if 'Year' in sales_full.columns and 'Quarter' in sales_full.columns:
            quarterly_revenue = sales_full.groupby(['Year', 'Quarter'])['SubTotal'].sum().to_dict()
            quarterly_revenue = {f"{k[0]}-Q{k[1]}": float(v) for k, v in quarterly_revenue.items()}
        
        # Financial health score (0-100)
        health_score = min(100, (
            (50 if gross_margin > 20 else gross_margin * 2.5) +
            (30 if revenue_per_employee > 100000 else revenue_per_employee / 100000 * 30) +
            (20 if total_revenue > 1000000 else total_revenue / 1000000 * 20)
        ))
        
        # Assemble finance data
        self.finance_data = {
            'summary': {
                'total_revenue': round(total_revenue, 2),
                'total_tax': round(total_tax, 2),
                'total_freight': round(total_freight, 2),
                'total_gross_profit': round(total_gross_profit, 2),
                'gross_margin_percentage': round(gross_margin, 2),
                'effective_tax_rate': round(tax_rate, 2),
                'revenue_per_employee': round(revenue_per_employee, 2),
                'financial_health_score': round(health_score, 1)
            },
            'by_year': sales_full.groupby('Year')['SubTotal'].sum().to_dict() if 'Year' in sales_full.columns else {},
            'by_quarter': quarterly_revenue,
            'by_month': monthly_revenue,
            'insights': [
                f"Total Revenue: ${total_revenue:,.2f}",
                f"Gross Margin: {gross_margin:.2f}%",
                f"Revenue per Employee: ${revenue_per_employee:,.2f}",
                f"Financial Health Score: {health_score:.1f}/100",
                f"Effective Tax Rate: {tax_rate:.2f}%"
            ],
            'recommendations': self._generate_finance_recommendations(
                gross_margin, revenue_per_employee, health_score
            )
        }
        
        print("✓ Finance data transformation completed")
        return self.finance_data
    
    def _generate_hr_recommendations(self, high_risk_pct, avg_tenure, diversity_ratio):
        """Generate HR recommendations based on metrics"""
        recommendations = []
        
        if high_risk_pct > 20:
            recommendations.append("High attrition risk detected. Consider employee engagement initiatives and compensation review.")
        
        if avg_tenure < 3:
            recommendations.append("Low average tenure indicates retention challenges. Review onboarding and career development programs.")
        
        if diversity_ratio < 40:
            recommendations.append("Gender diversity is below optimal levels. Implement inclusive hiring practices.")
        
        if not recommendations:
            recommendations.append("HR metrics are healthy. Continue monitoring and maintain current practices.")
        
        return recommendations
    
    def _generate_finance_recommendations(self, margin, rev_per_emp, health_score):
        """Generate finance recommendations based on metrics"""
        recommendations = []
        
        if margin < 15:
            recommendations.append("Gross margin is below target. Review pricing strategy and cost optimization opportunities.")
        
        if rev_per_emp < 80000:
            recommendations.append("Revenue per employee is low. Consider productivity improvements and workforce optimization.")
        
        if health_score < 50:
            recommendations.append("Financial health score indicates concerns. Prioritize revenue growth and cost management.")
        elif health_score > 80:
            recommendations.append("Excellent financial health. Explore growth investment opportunities.")
        
        return recommendations
    
    def load(self, output_path: str = "./data/processed/"):
        """Load transformed data into JSON files"""
        print("\n" + "="*60)
        print("STEP 4: LOADING DATA")
        print("="*60)
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save to JSON files
        with open(f"{output_path}sales_kpis.json", 'w') as f:
            json.dump(self.sales_data, f, indent=2, default=str)
        print(f"  ✓ Saved: {output_path}sales_kpis.json")
        
        with open(f"{output_path}hr_kpis.json", 'w') as f:
            json.dump(self.hr_data, f, indent=2, default=str)
        print(f"  ✓ Saved: {output_path}hr_kpis.json")
        
        with open(f"{output_path}finance_kpis.json", 'w') as f:
            json.dump(self.finance_data, f, indent=2, default=str)
        print(f"  ✓ Saved: {output_path}finance_kpis.json")
        
        print("\n✓ Data loading completed successfully")
        return True
    
    def generate_summary_report(self):
        """Generate a summary report of the ETL process"""
        print("\n" + "="*60)
        print("ETL SUMMARY REPORT")
        print("="*60)
        
        print("\n📊 SALES METRICS:")
        for insight in self.sales_data['insights']:
            print(f"  • {insight}")
        
        print("\n👥 HR METRICS:")
        for insight in self.hr_data['insights']:
            print(f"  • {insight}")
        
        print("\n💰 FINANCE METRICS:")
        for insight in self.finance_data['insights']:
            print(f"  • {insight}")
        
        print("\n📋 RECOMMENDATIONS:")
        print("\nHR Recommendations:")
        for rec in self.hr_data['recommendations']:
            print(f"  • {rec}")
        
        print("\nFinance Recommendations:")
        for rec in self.finance_data['recommendations']:
            print(f"  • {rec}")
    
    def run_pipeline(self):
        """Execute full ETL pipeline"""
        print("\n" + "="*60)
        print("ADVENTUREWORKS ADVANCED ETL PIPELINE")
        print("="*60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Extract
        if not self.extract():
            print("\n❌ ETL Pipeline failed at extraction stage")
            return False
        
        # Clean and preprocess
        self.clean_and_preprocess()
        
        # Transform
        self.transform_sales_data()
        self.transform_hr_data()
        self.transform_finance_data()
        
        # Load
        self.load()
        
        # Generate summary
        self.generate_summary_report()
        
        print("\n" + "="*60)
        print("✓ ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True


# Main execution
if __name__ == "__main__":
    # Initialize ETL pipeline
    etl = AdventureWorksETL(data_path="./data/raw/")
    
    # Run the complete pipeline
    success = etl.run_pipeline()
    
    if success:
        print("\n✅ All data files are ready for agent consumption!")
        print("\nNext steps:")
        print("  1. Check ./data/processed/ for generated JSON files")
        print("  2. Update your agents to load these KPI files")
        print("  3. Test agent responses with the enriched data")
    else:
        print("\n❌ Pipeline failed. Please check error messages above.")
