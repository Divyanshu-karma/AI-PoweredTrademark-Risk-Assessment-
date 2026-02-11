# src/rag/input_adapter.py

def structured_object_to_query(app) -> str:

    goods_section = ""
    for cls, desc in app.goods_map.items():
        goods_section += f"\nClass {cls}: {desc}"

    query = (
        f"Trademark Application Analysis Request:\n\n"
        f"Mark: {app.mark}\n"
        f"Mark Type: {app.mark_type}\n"
        f"Register: {app.register}\n\n"
        f"Filing Basis: {app.filing_basis}\n"
        f"Use in Commerce: {app.use_in_commerce}\n\n"
        f"Owner Name: {app.owner_name}\n"
        f"Entity Type: {app.owner_entity}\n"
        f"Citizenship: {app.owner_citizenship}\n\n"
        f"Serial Number: {app.serial_number}\n"
        f"Registration Number: {app.registration_number}\n\n"
        f"Goods and Services:{goods_section}\n\n"
        f"Analyze the application strictly under TMEP guidelines "
        f"for potential examination issues."
    )

    return query
