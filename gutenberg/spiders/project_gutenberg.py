import scrapy, requests

from gutenberg.items import GutenbergEbook

class GutenbergSpider(scrapy.Spider):
    name = "project_gutenberg"
    allowed_domains = ["www.gutenberg.org"]
    start_urls = ["https://www.gutenberg.org/ebooks/bookshelf"]
    index = 0
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_bookshelves)
    
    def parse_bookshelves(self, response):
        bookshelves = response.css("div.bookshelves")
        bookshelves_links = bookshelves.css("ul > li > a::attr(href)").getall()
        
        for link in bookshelves_links:
            bookshelf_name = link.split("/")[-1]
            yield scrapy.Request(link, callback=self.parse_ebooks, meta={"bookshelf_name": bookshelf_name})
            
    def parse_ebooks(self, response, bookshelf_name):
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
            ebook["bookshelf_name"] = bookshelf_name
            ebook["title"] = content.css("span.title::text").get()
            ebook["author"] = content.css("span.subtitle::text").get()
            ebook["downloads"] = content.css("span.extra::text").get()
            ebook["text"] = text
            ebook["text_file"] = f"https://www.gutenberg.org/ebooks/{id}.txt.utf-8"
            
            yield ebook
            
            self.index += 1
            
        yield scrapy.Request(f"https://www.gutenberg.org/ebooks/bookshelf/57?start_index={self.index}", callback=self.parse)
