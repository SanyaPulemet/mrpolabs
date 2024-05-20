from fastapi.responses import JSONResponse
from sqlalchemy import select
from basecontroller import BaseController # base
from fastapi import Depends
from db_init import create_connection
from sqla import * # сущности
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime
from services import * # logic


class orderInputForm(BaseModel):
    delivery_address: str


class MainController(BaseController):
    def _register_routes(self):
        @self.router.get('/init')
        async def initData(
                session: AsyncSession = Depends(create_connection)
        ) -> JSONResponse:
            async with session.begin():
                client1 = ClientDB(name="client1",phone="phone")
                courier1 = CourierDB(name="client1")
                comment1 = CommentDB(text="txt")
                order1 = OrderDB()

                session.add_all([client1,courier1,comment1,order1])
                await session.commit()

            return JSONResponse(content={'text': 'data added', 'code': 200})

        @self.router.post('/make-order')
        async def makeOrder(
                user_id: int,
                form_data: orderInputForm,
                session: AsyncSession = Depends(create_connection)
        ) -> JSONResponse:
            order_data = {}
            async with session.begin():
                query = select(ClientDB).where(ClientDB.id == user_id)
                query_result = await session.execute(query)
                user: ClientDB = query_result.scalars().one_or_none()
                if user is None:
                    await session.rollback()
                    return JSONResponse(content={'error': 'User not found'}, status_code=404)

                order = await make_order(user, form_data.delivery_address, [])
                session.add(order)
                await session.commit()
                order_data = order.JSONify

            return JSONResponse(content={'order': order_data})

        @self.router.post('/mark-order')
        async def markOrder(
                order_id: int,
                courier_id: int,
                session: AsyncSession = Depends(create_connection)
        ) -> JSONResponse:
            order_data = {}
            async with session.begin():
                query = select(OrderDB).where(OrderDB.id == order_id)
                query_result = await session.execute(query)
                order: OrderDB = query_result.scalars().one_or_none()
                query = select(CourierDB).where(CourierDB.id == courier_id)
                query_result = await session.execute(query)
                courier: CourierDB = query_result.scalars().one_or_none()
                if order is None or courier is None:
                    await session.rollback()
                    return JSONResponse(content={'error': 'not found'}, status_code=404)
                await mark_order_as_taken(order, courier)
                await session.commit()
                order_data = order.JSONify

            return JSONResponse(content={'order': order_data, 'code': 200})

        @self.router.post('/mark-order-as-d')
        async def markOrderAsD(
                order_id: int,
                courier_id: int,
                session: AsyncSession = Depends(create_connection)
        ) -> JSONResponse:
            order_data = {}
            async with session.begin():
                query = select(OrderDB).where(OrderDB.id == order_id)
                query_result = await session.execute(query)
                order: OrderDB = query_result.scalars().one_or_none()
                query = select(CourierDB).where(CourierDB.id == courier_id)
                query_result = await session.execute(query)
                courier: CourierDB = query_result.scalars().one_or_none()
                if order is None or courier is None:
                    await session.rollback()
                    return JSONResponse(content={'error': 'not found'}, status_code=404)
                await mark_order_as_delivered(order, courier)
                await session.commit()
                order_data = order.JSONify

            return JSONResponse(content={'order': order_data, 'code': 200})

        @self.router.post('/leave-comment')
        async def leaveComment(
                order_id: int,
                user_id: int,
                comment_text: str,
                session: AsyncSession = Depends(create_connection)
        ) -> JSONResponse:
            comment_data = {}
            async with session.begin():
                query = select(OrderDB).where(OrderDB.id == order_id)
                query_result = await session.execute(query)
                order: OrderDB = query_result.scalars().one_or_none()
                query = select(ClientDB).where(ClientDB.id == user_id)
                query_result = await session.execute(query)
                user: ClientDB = query_result.scalars().one_or_none()
                if order is None or user is None:
                    await session.rollback()
                    return JSONResponse(content={'error': 'not found'}, status_code=404)
                comment = await leave_comment(order, user, comment_text)
                session.add(comment)
                await session.commit()
                comment_data = comment.JSONify

            return JSONResponse(content={'comment': comment_data, 'code': 200})

        @self.router.post('/check-delivery-time')
        async def checkDelTime(
                order_id: int,
                session: AsyncSession = Depends(create_connection)
        ) -> JSONResponse:
            order_data = {}
            async with session.begin():
                query = select(OrderDB).where(OrderDB.id == order_id)
                query_result = await session.execute(query)
                order: OrderDB = query_result.scalars().one_or_none()
                if order is None:
                    await session.rollback()
                    return JSONResponse(content={'error': 'not found'}, status_code=404)
                await check_delivery_time(order)
                await session.commit()
                order_data = order.JSONify

            return JSONResponse(content={'order': order_data, 'code': 200})

main_controller = MainController(routes_prefix='/')
