"""
Environment configuration для Behave BDD тестів
"""

def before_all(context):
    """Виконується один раз перед усіма тестами"""
    context.config.setup_logging()
    print("🚀 Запуск BDD тестів Quizizz")


def before_feature(context, feature):
    """Виконується перед кожним feature файлом"""
    print(f"\n📋 Тестування функціоналу: {feature.name}")


def before_scenario(context, scenario):
    """Виконується перед кожним сценарієм"""
    context.test_data = {}
    context.search_results = []


def after_scenario(context, scenario):
    """Виконується після кожного сценарію"""
    if scenario.status == "failed":
        print(f"❌ Сценарій провалився: {scenario.name}")
    else:
        print(f"✅ Сценарій пройдено: {scenario.name}")


def after_all(context):
    """Виконується один раз після всіх тестів"""
    print("\n🏁 BDD тести завершено")
