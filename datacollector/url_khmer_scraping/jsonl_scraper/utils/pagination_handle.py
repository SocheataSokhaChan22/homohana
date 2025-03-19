"""
This Class using for handle the pagination pages for websites.
"""


class PaginationHandle:
    """
    A class to handle pagination for website URLs.
    """
    @staticmethod
    def get_next_page_url_with_param(current_url):
        """
        Generate the URL for the next page based on the current URL's query parameters.
        Args:
        -----------
        current_url: list
            The current URL, which may include query parameters.
        Returns:
        -----------
        next_page: str
            The URL for the next page, updated with the correct page number.
        """
        if "?" in current_url:
            base_url, query_string = current_url.split("?", 1)
            query_params = query_string.split("&")
            new_query_params = []

            for param in query_params:
                if param.startswith("page="):
                    page_num = int(param.split("=")[1]) + 1
                    new_query_params.append(f"page={page_num}")
                else:
                    new_query_params.append(param)

            next_page = base_url + "?" + "&".join(new_query_params)
        else:
            next_page = current_url + "?page=2"

        return next_page

    @staticmethod
    def get_next_page_url(url):
        """
        Generate the URL for the next page based on the current URL's.
        Args:
        -----------
        current_url: str
            The current URL, which may include query parameters.
        Returns:
        -----------
        next_page_url: str
            The URL for the next page, updated with the correct page number.
        """
        current_url = url.rstrip("/").split("/")
        if current_url[-1].isdigit():
            current_url[-1] = str(int(current_url[-1]) + 1)
        else:
            current_url.append("page/2")
        next_page_url = "/".join(current_url)

        return next_page_url
