from django.core.management.base import BaseCommand
from django.utils import timezone

from storage.models import AboutUs, Text, Warehouse, WarehouseImage

faq_data = {
    "О складах и боксах": [
        {
            "question": "Как устроены склады индивидуального хранения SelfStorage?",
            "answer": "Каждый склад сети SelfStorage – это отапливаемое и сухое помещение, оборудованное боксами различных размеров, которые вы можете арендовать для хранения вещей на любой срок от 1 месяца",
        },
        {
            "question": "Какие условия хранения поддерживаются в складах SelfStorage?",
            "answer": "Во всех филиалах Кладовкин регулярно проводится уборка помещений, а также поддерживается постоянная температура и уровень влажности.",
        },
        {
            "question": "Что нельзя хранить в боксах SelfStorage?",
            "answer": "Мы не принимаем на хранение следующие позиции:\nтоксичные и радиоактивные вещества\n/"
            "материалы, источающие дым и запах;\n/"
            "легковоспламеняющиеся материалы и жидкости;\n/"
            "запрещенные к обороту в РФ предметы;\n/"
            "оружие и взрывоопасные вещества;\n/"
            "деньги и ценные бумаги;\n/"
            "продукты питания;\n/"
            "растения и животные;\n/"
            "лекарственные препараты в любой форме.",
        },
    ],
    "Доступ к складам и боксам": [
        {
            "question": "Как осуществляется доступ к боксу?",
            "answer": "Бокс – это ваш личный мини-склад, расположенный в складском комплексе SelfStorage./"
            "В полностью автоматизированных складах боксы оборудованы электронной системой доступа по пин-коду, который вы получите по СМС сразу после заключения договора аренды. Пин-код нужно будет ввести в специальный терминал на территории складского комплекса, после чего доступ к вашему личному мини-складу будет открыт./"
            "В складах с администратором боксы закрываются на навесной замок, ключ от которого находиться только у арендатора. Вы можете использовать свой замок или приобрести новый прямо на складе, наши менеджеры помогут вам с выбором.",
        },
        {
            "question": "Как осуществляется доступ к складскому комплексу?",
            "answer": "Все наши складские комплексы оборудованы электронной системой доступа. Оформив договор аренды онлайн, вы получите СМС на свой телефон с персональным кодом доступа к складу. Полученный пин-код нужно будет ввести в специальное поле в мобильном приложении или в терминал, расположенный рядом с входной дверью в комплекс,/"
            "после чего доступ будет открыт. Код доступа вы всегда сможете найти в своём личном кабинете на сайте или в мобильном приложении.",
        },
        {
            "question": "Что произойдет, если я забуду свой пин-код?",
            "answer": "Вы всегда можете найти код доступа в своем личном кабинете сайте или в мобильном приложении. Если вы утратите доступ к своему личному кабинету, мы поможем вам восстановить аккаунт и обновим пин-код в целях безопасности.",
        },
    ],
    "Договор аренды и оплата": [
        {
            "question": "Как арендовать помещение для хранения в SelfStorage?",
            "answer": 'Чтобы арендовать бокс, вам нужно зарегистрироваться в личном кабинете, выбрать подходящий тариф и оплатить услуги. Всё это вы можете сделать онлайн, по телефону службы круглосуточной заботы о клиентах Кладовкин или в нашем офисе.Чтобы узнать подробнее о процедуре аренды бокса, переходите на страницу "Как выбрать бокс" или получите консультацию специалиста.',
        },
        {
            "question": "Какой минимальный и максимальный срок аренды бокса?",
            "answer": "Вы можете арендовать бокс на любой срок от 1 месяца. Договор аренды заключается на срок до 11 месяцев с последующим автоматическим продлением до того момента, пока вы не захотите его расторгнуть.",
        },
        {
            "question": "Как и когда можно расторгнуть договор аренды?",
            "answer": "Договор может быть расторгнут в любое время. Для этого вам нужно освободить помещение и оставить его открытым, после чего нажать кнопку «Закрыть договор» в личном кабинете или сообщить о расторжении договора менеджеру службы круглосуточной заботы о клиентах. Мы проверим бокс и вернем вам депозит в течение 10 рабочих дней с момента закрытия договора.",
        },
    ],
}

warehouses_data = [
    {
        "city": "Москва",
        "address": "ул. Рокотова, д. 15",
        "number_of_boxes": 390,
        "creation_date": timezone.now(),
        "price_per_month": 3040,
        "preview_image": "image9.png",
        "description": "Рядом с метро",
        "temperature": 17,
        "ceiling_height": 3,
        "full_description": "Полное описание",
        "warehouseImage": ["image2.png", "photo8.png"]
    },
    {
        "city": "Одинцово",
        "address": "ул. Северная, д. 36",
        "number_of_boxes": 258,
        "creation_date": timezone.now(),
        "price_per_month": 2264,
        "preview_image": "image11.png",
        "description": "Парковка",
        "temperature": "18",
        "ceiling_height": "3",
        "full_description": "Полное описание",
        "warehouseImage": ["image2.png", "photo8.png"]
    },
    {
        "city": "Пушкино",
        "address": "ул. Строителей, д. 5",
        "number_of_boxes": 361,
        "creation_date": timezone.now(),
        "price_per_month": 2154,
        "preview_image": "image15.png",
        "description": "Высокие потолки",
        "temperature": 20,
        "ceiling_height": 5,
        "full_description": "Полное описание",
        "warehouseImage": ["image2.png", "photo8.png"]
    },
    {
        "city": "Люберцы",
        "address": "ул. Советская, д. 88",
        "number_of_boxes": 130,
        "creation_date": timezone.now(),
        "price_per_month": 1408,
        "preview_image": "image16.png",
        "description": "Осталось мало боксов",
        "temperature": 18,
        "ceiling_height": 3,
        "full_description": "Полное описание",
        "warehouseImage": ["image2.png", "photo8.png"]
    },
    {
        "city": "Домодедово",
        "address": "ул. Орджоникидзе, д. 29",
        "number_of_boxes": 234,
        "creation_date": timezone.now(),
        "price_per_month": 2978,
        "preview_image": "image151.png",
        "description": "Большие боксы",
        "temperature": 21,
        "ceiling_height": 4,
        "full_description": "Полное описание",
        "warehouseImage": ["image2.png", "photo8.png"]
    }
]


class Command(BaseCommand):
    help = "Заполнить базу данных"

    def handle(self, *args, **kwargs):
        for title, questions in faq_data.items():
            about_us, _ = AboutUs.objects.get_or_create(title=title)
            for q_and_a in questions:
                question = q_and_a["question"]
                answer = q_and_a["answer"]
                Text.objects.get_or_create(
                    title=about_us, question=question, answer=answer
                )

        for warehouse_info in warehouses_data:
            warehouse, _ = Warehouse.objects.get_or_create(
                city=warehouse_info['city'],
                address=warehouse_info['address'],
                number_of_boxes=warehouse_info['number_of_boxes'],
                price_per_month=warehouse_info['price_per_month'],
                preview_image=warehouse_info['preview_image'],
                description=warehouse_info['description'],
                temperature=warehouse_info['temperature'],
                ceiling_height=warehouse_info['ceiling_height'],
                full_description=warehouse_info['full_description'],
            )
            for image_name in warehouse_info['warehouseImage']:
                WarehouseImage.objects.get_or_create(
                    warehouse=warehouse,
                    full_image=image_name
                )


        self.stdout.write(self.style.SUCCESS("База данных заполнена"))
