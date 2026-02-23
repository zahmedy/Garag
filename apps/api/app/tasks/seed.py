from sqlmodel import Session, select
from app.db.session import engine
from app.models.car import CarMake, CarModel

def seed():
    makes = [
        ("Toyota", "toyota", ["Camry", "Corolla", "Land Cruiser", "Hilux"]),
        ("Hyundai", "hyundai", ["Elantra", "Sonata", "Tucson", "Santa Fe"]),
        ("Kia", "kia", ["K5", "Sportage", "Sorento", "Cerato"]),
    ]

    with Session(engine) as s:
        for make_name, make_slug, models in makes:
            make = s.exec(select(CarMake).where(CarMake.slug == make_slug)).first()
            if not make:
                make = CarMake(name=make_name, slug=make_slug)
                s.add(make)
                s.commit()
                s.refresh(make)

            for model_name in models:
                model_slug = model_name.lower().replace(" ", "-")
                exists = s.exec(
                    select(CarModel).where(CarModel.make_id == make.id, CarModel.slug == model_slug)
                ).first()
                if not exists:
                    s.add(CarModel(make_id=make.id, name=model_name, slug=model_slug))
        s.commit()

if __name__ == "__main__":
    seed()
    print("seeded")