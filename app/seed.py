from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.models import Activity, Building, Organization, OrganizationPhone


def seed_data() -> None:
    engine = create_engine(settings.database_url, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Building).first():
            return

        building_1 = Building(
            address="г. Москва, ул. Ленина 1, офис 3",
            latitude=55.7558,
            longitude=37.6176,
        )
        building_2 = Building(
            address="г. Новосибирск, ул. Блюхера 32/1",
            latitude=54.9833,
            longitude=82.8964,
        )
        building_3 = Building(
            address="г. Екатеринбург, ул. Малышева 51",
            latitude=56.8389,
            longitude=60.6057,
        )

        food = Activity(name="Еда", level=1)
        meat = Activity(name="Мясная продукция", level=2, parent=food)
        dairy = Activity(name="Молочная продукция", level=2, parent=food)

        cars = Activity(name="Автомобили", level=1)
        trucks = Activity(name="Грузовые", level=2, parent=cars)
        passenger = Activity(name="Легковые", level=2, parent=cars)
        parts = Activity(name="Запчасти", level=3, parent=passenger)
        accessories = Activity(name="Аксессуары", level=3, parent=passenger)

        org_1 = Organization(name='ООО "Рога и Копыта"', building=building_2)
        org_1.phones = [
            OrganizationPhone(phone="2-222-222"),
            OrganizationPhone(phone="3-333-333"),
            OrganizationPhone(phone="8-923-666-13-13"),
        ]
        org_1.activities = [meat, dairy]

        org_2 = Organization(name="Мясной Дом", building=building_1)
        org_2.phones = [OrganizationPhone(phone="8-495-000-00-00")]
        org_2.activities = [meat]

        org_3 = Organization(name="АвтоСнаб", building=building_3)
        org_3.phones = [OrganizationPhone(phone="8-343-111-22-33")]
        org_3.activities = [parts, accessories]

        org_4 = Organization(name="ГрузАвто", building=building_3)
        org_4.phones = [OrganizationPhone(phone="8-343-444-55-66")]
        org_4.activities = [trucks]

        db.add_all(
            [
                building_1,
                building_2,
                building_3,
                food,
                cars,
                org_1,
                org_2,
                org_3,
                org_4,
            ]
        )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
