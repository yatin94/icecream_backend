# app/api/endpoints/topping.py
from fastapi import APIRouter, HTTPException
from typing import List
from database import SessionDep
from sqlalchemy import text
from sqlmodel import select
from models.sales import BillItems

router = APIRouter()

month_names = {
    '01': "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}



@router.get("/analytics/summary")
async def get_total_sales(session:SessionDep) -> dict:
    return_data = {
        "total_ice_creams_sold": 0,
        "total_sales_amount": 0,
        "total_expenses_amount": 0,
        "total_cones_sold": 0,
        "total_sundae_sold": 0
    }
    len_statement = text("select count(*) from BillItems")
    sales_amount_statement = text("select sum(total_bill) as total_sales_amount from Bill")
    total_expense_amount = text("select sum(total_cost) as total_expenses_amount from Purchases where is_deleted=0")
    total_cones_sold_statement = text("select count(BillItems.id) from BillItems join IceCreamType on BillItems.flavor_type == IceCreamType.id where IceCreamType.type == 'Cone'")
    total_sundae_sold_statement = text("select count(BillItems.id) from BillItems join IceCreamType on BillItems.flavor_type == IceCreamType.id where IceCreamType.type == 'Sundae'")
    return_data['total_ice_creams_sold'] = session.exec(len_statement).scalar()
    return_data['total_sales_amount'] = session.exec(sales_amount_statement).scalar()
    return_data['total_expenses_amount'] = session.exec(total_expense_amount).scalar()
    return_data['total_cones_sold'] = session.exec(total_cones_sold_statement).scalar()
    return_data['total_sundae_sold'] = session.exec(total_sundae_sold_statement).scalar()
    return return_data





@router.get("/analytics/monthly_earnings")
async def get_total_sales(session:SessionDep) -> dict:
    return_data = []
    a = text(f"""
        SELECT 
            COALESCE(Bill.MonthYear, Purchases.MonthYear) as MonthYear,
            COALESCE(TotalSales, 0) as TotalSales,
            COALESCE(TotalExpense, 0) as TotalExpense
        FROM
            (SELECT 
                strftime('%m-%Y', created_at) AS MonthYear,
                SUM(total_bill) AS TotalSales
            FROM 
                Bill
            GROUP BY 
                strftime('%m-%Y', created_at)
            ) Bill
        LEFT JOIN
            (SELECT
                strftime('%m-%Y', created_at) AS MonthYear,
                SUM(total_cost) AS TotalExpense
            FROM 
                Purchases
            WHERE
                Purchases.is_deleted = 0
            GROUP BY 
                strftime('%m-%Y', created_at)
            ) Purchases
        ON 
            Bill.MonthYear = Purchases.MonthYear
    """)
    results = session.exec(a).all()
    print(results)
    for result in results:
        month_name, month_year = result[0].split("-")
        month_name = month_names[month_name]
        return_data.append(
        {"month": f"{month_name}-{month_year}", "earnings": result[1], "expense": result[2], "profit":result[1]-result[2]},
        )
    return {"data":return_data}
    return {
  "data": [
    {"month": "January", "earnings": 1234, "expense": 1324, "profit":12},
    {"month": "February", "earnings": 2345, "expense": 1324, "profit":12}
  ]
}


@router.get("/analytics/{type}")
async def get_type_sale_summary(type:str, session:SessionDep) -> List[dict]:
    return_data = []
    total_cones_sold_statement = text(f"""
            select Flavors.flavor_name, IceCreamSize.name, count(BillItems.id), sum(BillItems.base_price) from BillItems 
            join Flavors on BillItems.flavor_id == Flavors.id 
            join IceCreamSize on IceCreamSize.id == BillItems.flavor_size
            join IceCreamType on IceCreamType.id == BillItems.flavor_type
            where IceCreamType.type = '{type.capitalize()}'
            group by Flavors.flavor_name
    """)
    sql_results = session.exec(total_cones_sold_statement).all()
    for sql_result in sql_results:
        return_data.append(
            {"flavor":sql_result[0], "size":sql_result[1], "count":sql_result[2], "total_earnings":sql_result[3]}
        )
    return return_data



@router.get("/analytics/total_purchases_amount")
async def get_total_sales(session:SessionDep) -> dict:
    return {"total_amount": 1000}


@router.get("/analytics/get_sales_by_types")
async def get_total_sales(session:SessionDep) -> dict:
    return {"cone": [], "sundae": [], "cone_sales_amount": 0, "sundae_sales_amount": 1}

