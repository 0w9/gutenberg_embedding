import scrapy, requests

from gutenberg.items import GutenbergEbook

class GutenbergSpider(scrapy.Spider):
    name = "project_gutenberg"
    allowed_domains = ["www.gutenberg.org"]
    start_urls = ["https://www.gutenberg.org/ebooks/bookshelf/57"]
    index = 0

    def parse(self, response):
        results = response.css("ul.results")
        
        if not results:
            return
        
        books = results.css("li.booklink")
        
        for book in books:
            content = book.css("span.content")
            link = book.css("a.link::attr(href)").get()
            id = link.split("/ebooks/")[1]
            text = requests.get(f"https://www.gutenberg.org/ebooks/{id}.txt.utf-8").text
            
            ebook = GutenbergEbook()
            ebook["index"] = self.index
            ebook["id"] = id
            ebook["title"] = content.css("span.title::text").get()
            ebook["author"] = content.css("span.subtitle::text").get()
            ebook["downloads"] = content.css("span.extra::text").get()
            ebook["text"] = text
            ebook["text_file"] = f"https://www.gutenberg.org/ebooks/{id}.txt.utf-8"
            
            yield ebook
            
            self.index += 1
            
        yield scrapy.Request(f"https://www.gutenberg.org/ebooks/bookshelf/57?start_index={self.index}", callback=self.parse)
