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


async def add_date_filter(start_date: str | None, end_date: str|None, sql_stmt: str, has_where: bool = False):
    if not has_where and (start_date or end_date):
        sql_stmt = sql_stmt + " where "
    if has_where and (start_date or end_date):
        print("adding and")
        print(start_date, end_date)
        sql_stmt = sql_stmt + ' and '
    
    if start_date:
        sql_stmt += f" created_at >= '{start_date}'"
    if end_date and not start_date:
        sql_stmt += f" created_at <= '{end_date}'"
    elif end_date and start_date:
        sql_stmt += f" and created_at <= '{end_date}'"
    return sql_stmt

@router.get("/analytics/summary")
async def get_sales_summary(session:SessionDep, start_date: str | None = None, end_date: str | None = None) -> dict:
    return_data = {
        "total_ice_creams_sold": 0,
        "total_sales_amount": 0,
        "total_expenses_amount": 0,
        "total_cones_sold": 0,
        "total_sundae_sold": 0
    }
    len_statement = await add_date_filter(start_date, end_date, "select count(*) from BillItems")
    print(len_statement)
    return_data['total_ice_creams_sold'] = session.exec(text(len_statement)).scalar()

    sales_amount_statement = await add_date_filter(start_date, end_date, "select sum(total_bill) as total_sales_amount from Bill")
    return_data['total_sales_amount'] = session.exec(text(sales_amount_statement)).scalar()

    total_expense_amount = await add_date_filter(start_date, end_date, "select sum(total_cost) as total_expenses_amount from Purchases where is_deleted=0", has_where=True)
    return_data['total_expenses_amount'] = session.exec(text(total_expense_amount)).scalar()

    total_cones_sold_statement = await add_date_filter(start_date, end_date, "select count(BillItems.id) from BillItems join Flavors on BillItems.flavor_id == Flavors.id where Flavors.is_sundae == 0", True)
    return_data['total_cones_sold'] = session.exec(text(total_cones_sold_statement)).scalar()

    total_sundae_sold_statement = await add_date_filter(start_date, end_date, "select count(BillItems.id) from BillItems join Flavors on BillItems.flavor_id == Flavors.id where Flavors.is_sundae == 1", True)
    return_data['total_sundae_sold'] = session.exec(text(total_sundae_sold_statement)).scalar()
    return return_data





@router.get("/analytics/monthly_earnings")
async def get_monthly_earnings(session:SessionDep) -> dict:
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
async def get_type_sale_summary(type:str, session:SessionDep, start_date: str | None = None, end_date: str | None = None) -> List[dict]:
    return_data = []
    if type == "sundae":
        is_sundae = 1
    else:
        is_sundae = 0
    where_clause = f" where Flavors.is_sundae = {is_sundae}"
    if start_date:
        where_clause += f" AND BillItems.created_at >= '{start_date}'"
    if end_date:
        where_clause += f" AND BillItems.created_at <= '{end_date}'"

    total_cones_sold_statement = f"""
            select Flavors.flavor_name, IceCreamSize.name, count(BillItems.id), sum(BillItems.base_price) from BillItems 
            join Flavors on BillItems.flavor_id == Flavors.id 
            join IceCreamSize on IceCreamSize.id == BillItems.flavor_size
            {where_clause}
            group by Flavors.flavor_name, IceCreamSize.name
    """
    print(total_cones_sold_statement)
    sql_results = session.exec(text(total_cones_sold_statement)).all()
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

