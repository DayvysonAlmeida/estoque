from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # Quantidade padrão de itens por página
    page_size_query_param = 'page_size'  # Permite que o cliente solicite uma página maior ou menor
    max_page_size = 50  # Quantidade máxima de itens por página
