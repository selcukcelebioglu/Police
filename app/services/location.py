from fastapi import Header


def resolve_location(
    city: str | None,
    district: str | None,
    x_city: str | None = Header(default=None),
    x_district: str | None = Header(default=None),
) -> tuple[str, str]:
    final_city = city or x_city or "Bilinmiyor"
    final_district = district or x_district or "Bilinmiyor"
    return final_city.strip(), final_district.strip()
