from random import randint 
from functools import wraps
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, PrimaryKeyConstraint, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import time
from datetime import datetime, timedelta

Base = declarative_base()

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/lysenko"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
    phone_number = Column(String(13), nullable=False)

    rooms = relationship('Room', back_populates='user')
    ordering_services = relationship('OrderingService', back_populates='user')

class Service(Base):
    __tablename__ = 'services'

    service_id = Column(Integer, primary_key=True, nullable=False)
    sirvice_name = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)

    ordering_services = relationship('OrderingService', back_populates='service')

class OrderingService(Base):
    __tablename__ = 'ordering_services'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    service_id = Column(Integer, ForeignKey('services.service_id'), primary_key=True, nullable=False)
    data = Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)

    user = relationship('Users', back_populates='ordering_services')
    service = relationship('Service', back_populates='ordering_services')

class RoomType(Base):
    __tablename__ = 'room_type'

    room_type_id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String(20), nullable=False)
    price = Column(Integer)

    rooms = relationship('Room', back_populates='room_type')

class Room(Base):
    __tablename__ = 'rooms'

    room_id = Column(Integer, primary_key=True, nullable=False)
    room_number = Column(Integer, nullable=False)
    room_type_id = Column(Integer, ForeignKey('room_type.room_type_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    check_in_date = Column(TIMESTAMP(timezone=True))
    check_out_date = Column(TIMESTAMP(timezone=True))

    user = relationship('Users', back_populates='rooms')
    room_type = relationship('RoomType', back_populates='rooms')

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        print(f"\nFunction '{func.__name__}' executed in {elapsed_time:.4f} milliseconds\n")
        return result
    return wrapper

class Model:
    # Дістати всі рядки
    @timeit
    def get_data(self, table_name):
        try:
            model_class = globals().get(table_name.title())
            if not model_class:
                raise ValueError(f"Table model {table_name} not found.")

            records = session.query(model_class).all()
            if records:
                return records
            else:
                print(f"No records found in {table_name}.")
        except Exception as e:
            print(f"Error fetching data from {table_name}: {str(e)}")
        return []


    # Перегляд даних із фільтрацією
    @timeit
    def get_data_in_range(self, table_name, id_field, id_start, id_end, order_field):
        try:
            
            model_class = globals().get(table_name.title())
            if not model_class:
                raise ValueError(f"Table model {table_name} not found.")
            query = session.query(model_class).filter(
                getattr(model_class, id_field).between(id_start, id_end)
            ).order_by(getattr(model_class, order_field))
            records = query.all()
            
            if records:
                return records
            else:
                print(f"No records found in {table_name} within the given range.")
        except Exception as e:
            print(f"Error fetching data from {table_name}: {str(e)}")
        return []


    # Пошук за шаблоном LIKE
    @timeit
    def get_data_by_field_like(self, table_name, req_field, search_req, order_field):
        try:
            model_class = globals().get(table_name.title())
            if not model_class:
                raise ValueError(f"Table model {table_name} not found.")
            
            query = session.query(model_class).filter(
                getattr(model_class, req_field).ilike(f"%{search_req}%")
            ).order_by(getattr(model_class, order_field))
            
            records = query.all()
            
            if records:
                return records
            else:
                print(f"No records found in {table_name} matching the search criteria.")
        except Exception as e:
            print(f"Error fetching data from {table_name}: {str(e)}")
        return []


    # Додавання запису в таблицю `users`
    @timeit
    def add_user(self, user_id, name, phone_number):
        try:
            user = Users(user_id=user_id, name=name, phone_number=phone_number)
            session.add(user)
            session.commit()
            print("User added successfully.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")


    # Генерація записів для `users`
    @timeit
    def generate_users(self, num_users):
        try:
            max_user_id = session.query(func.max(Users.user_id)).scalar() or 0

            for _ in range(num_users):
                user_id = max_user_id + 1
                name = f'User_{randint(1, 1000)}'
                phone_number = f'380{randint(1000000, 9999999)}'

                user = Users(user_id=user_id, name=name, phone_number=phone_number)
                session.add(user)
                max_user_id = user_id

            session.commit()
            print(f"{num_users} users generated successfully.")

        except Exception as e:
            session.rollback()
            print(f"Error generating users: {str(e)}")


    
    # Оновлення запису для таблиці `users`
    @timeit
    def update_user(self, user_id, name=None, phone_number=None):
        try:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            
            if user:
                if name:
                    user.name = name
                if phone_number:
                    user.phone_number = phone_number
                
                session.commit()
                print(f"User {user_id} updated successfully.")
            else:
                print(f"User with ID {user_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error updating user: {str(e)}")


    @timeit
    def add_service(self, service_id, service_name, price):
        try:
            service = Service(service_id=service_id, sirvice_name=service_name, price=price)
            session.add(service)
            session.commit()
            print("Service added successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error adding service: {str(e)}")


    @timeit
    def update_ordering_service(self, user_id, service_id, field, value):
        try:
            # Знаходимо запис для оновлення
            record = session.query(OrderingService).filter_by(user_id=user_id, service_id=service_id).first()

            if not record:
                print(f"Ordering service with user_id={user_id} and service_id={service_id} not found.")
                return

            if hasattr(record, field):
                setattr(record, field, value)
            else:
                print(f"Field '{field}' does not exist in OrderingService model.")

            # Застосовуємо зміни
            session.commit()
            print(f"Ordering service with user_id={user_id} and service_id={service_id} updated successfully.")

        except Exception as e:
            print(f"Error updating ordering service: {str(e)}")
            session.rollback()



    @timeit
    def generate_services(self, num_services):
        try:
            max_service_id = session.query(func.max(Service.service_id)).scalar() or 0

            for i in range(num_services):
                service_id = max_service_id + i + 1
                service_name = f'Service_{service_id}'
                price = randint(50, 500)

                service = Service(service_id=service_id, sirvice_name=service_name, price=price)
                session.add(service)

            session.commit()
            print(f"{num_services} services generated successfully.")

        except Exception as e:
            session.rollback()
            print(f"Error generating services: {str(e)}")



    @timeit
    def add_room(self, room_id, room_number, room_type_id, user_id, check_in_date, check_out_date):
        try:
            if user_id == "":
                user_id = None

            room = Room(
                room_id=room_id, 
                room_number=room_number, 
                room_type_id=room_type_id, 
                user_id=user_id, 
                check_in_date=check_in_date, 
                check_out_date=check_out_date
            )

            session.add(room)
            session.commit()
            print(f"Room {room_id} added successfully.")

        except Exception as e:
            session.rollback()
            print(f"Error adding room: {str(e)}")


    @timeit
    def update_room(self, room_id, field, new_value):
        try:
            room = session.query(Room).filter(Room.room_id == room_id).first()
            if room:
                setattr(room, field, new_value)
                session.commit()
                print(f"Room {room_id} updated successfully.")
            else:
                print(f"Room {room_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error updating room: {str(e)}")

    @timeit
    def generate_rooms(self, num_rooms):
        try:
            # Отримуємо максимальні значення для room_id, user_id, room_type_id
            max_room_id = session.query(func.max(Room.room_id)).scalar() or 0
            max_user_id = session.query(func.max(Users.user_id)).scalar() or 0
            max_room_type_id = session.query(func.max(RoomType.room_type_id)).scalar() or 0

            # Перевірка на наявність типів кімнат
            if max_room_type_id == 0:
                print("Error: No room types found in the database.")
                return

            # Генерація кімнат з випадковими даними
            rooms = []
            for _ in range(num_rooms):
                room_number = randint(1, 100)
                room_type_id = randint(1, max_room_type_id)
                user_id = randint(1, max_user_id) if max_user_id > 0 else None
                check_in_date = datetime.now() - timedelta(days=randint(1, 100)) + timedelta(hours=randint(0, 23))
                check_out_date = check_in_date + timedelta(days=randint(1, 30)) + timedelta(hours=randint(0, 23))

                room = Room(
                    room_id=max_room_id + 1,
                    room_number=room_number,
                    room_type_id=room_type_id,
                    user_id=user_id,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date
                )
                rooms.append(room)
                max_room_id += 1  # Збільшуємо максимальний room_id для наступної кімнати

            # Додавання кімнат в базу
            session.add_all(rooms)
            session.commit()
            print(f"{num_rooms} rooms generated successfully.")

        except Exception as e:
            session.rollback()
            print(f"Error generating rooms: {e}")

    @timeit
    def add_room_type(self, room_type_id, type, price):
        """Додавання нового типу кімнати до таблиці room_type."""
        try:
            # Створення нового об'єкта типу кімнати
            room_type = RoomType(
                room_type_id=room_type_id,
                type=type,
                price=price
            )
            
            # Додавання до бази даних
            session.add(room_type)
            session.commit()
            print(f"Room type {room_type_id} added successfully.")
            
        except Exception as e:
            session.rollback()
            print(f"Error adding room type: {e}")

    @timeit
    def update_room_type(self, room_type_id, field, new_value):
        """Оновлення даних типу кімнати в таблиці room_type."""
        try:
            # Оновлюємо тип кімнати через SQLAlchemy
            room_type = session.query(RoomType).filter(RoomType.room_type_id == room_type_id).first()
            
            if room_type:
                setattr(room_type, field, new_value)
                session.commit()
                print(f"Room type {room_type_id} updated successfully.")
            else:
                print(f"Room type {room_type_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error updating room type: {e}")

    @timeit
    def generate_room_types(self, num_room_types):
        """Генерація випадкових записів у таблиці room_type."""
        try:
            # Генерація типів кімнат через SQLAlchemy
            max_room_type_id = session.query(func.coalesce(func.max(RoomType.room_type_id), 0)).scalar()

            room_types = []
            for i in range(num_room_types):
                room_type = RoomType(
                    room_type_id=max_room_type_id + i + 1,
                    type=f"Type_{i + 1}",
                    price=randint(100, 1099)
                )
                room_types.append(room_type)
            
            session.add_all(room_types)
            session.commit()
            print(f"{num_room_types} room types generated successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error generating room types: {e}")

    @timeit
    def generate_ordering_services(self, num_services):
        """Генерація випадкових записів у таблиці ordering_services, гарантуючи унікальність пар user_id, service_id та дати."""
        try:
            # Перевіряємо максимальний service_id та user_id для унікальності
            max_service_id = session.query(func.coalesce(func.max(OrderingService.service_id), 0)).scalar()
            max_user_id = session.query(func.coalesce(func.max(OrderingService.user_id), 0)).scalar()

            # Отримуємо списки існуючих користувачів та сервісів
            users = session.query(Users).all()
            services = session.query(Service).all()

            # Перевірка, чи є користувачі та сервіси
            if not users or not services:
                print("Error: No users or services found in the database.")
                return

            ordering_services = []
            for i in range(num_services):
                # Вибір випадкових користувачів та сервісів
                user = users[randint(0, len(users) - 1)]
                service = services[randint(0, len(services) - 1)]

                # Генерація випадкової дати
                service_date = datetime.now() - timedelta(days=randint(1, 30))  # Випадкова дата за останні 30 днів

                # Створення унікального ключа для кожного запису
                ordering_service = OrderingService(
                    service_id=service.service_id,
                    user_id=user.user_id,
                    data=service_date  # Використовуємо дату як частину ключа
                )
                ordering_services.append(ordering_service)

            session.add_all(ordering_services)
            session.commit()
            print(f"{num_services} ordering services generated successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error generating ordering services: {e}")


    @timeit
    def add_ordering_service(self, user_id, service_id, date):
        """Додавання нового запису до таблиці ordering_services."""
        try:
            # Додавання нового замовлення через SQLAlchemy
            ordering_service = OrderingService(
                user_id=user_id,
                service_id=service_id,
                data=datetime.strptime(date, '%Y-%m-%d')
            )
            session.add(ordering_service)
            session.commit()
            print("Ordering service added successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error adding ordering service: {e}")


    @timeit
    def delete_data(self, table_name, record_id):
        """Видалення запису з будь-якої таблиці за назвою таблиці та ідентифікатором."""
        try:
            # Отримуємо клас таблиці з назви
            table_class = globals().get(table_name.capitalize())

            if not table_class:
                raise ValueError(f"Table {table_name} does not exist in the ORM mapping.")

            # Шукаємо запис за ідентифікатором
            record = session.query(table_class).get(record_id)

            if record:
                # Видаляємо запис
                session.delete(record)
                session.commit()
                print(f"Record with ID {record_id} deleted successfully from table {table_name}.")
            else:
                print(f"Record with ID {record_id} not found in table {table_name}.")

        except Exception as e:
            print(f"Error deleting record from table {table_name}: {str(e)}")
            session.rollback()
