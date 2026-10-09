from services.supabase_service import supabase

response = (
    supabase
    .table("operations")
    .select("*")
    .limit(1)
    .execute()
)

print(response.data)