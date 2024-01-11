class LocationEntry:
    def __init__(self,  name1, lat_long, amap_id, address, keyword2_count, name2, amap_link, baidu_link):
        self.name1 = name1
        self.lat_long = lat_long
        self.amap_id = amap_id
        self.address = address
        self.keyword2_count = keyword2_count
        self.name2 = name2
        self.amap_link = amap_link
        self.baidu_link = baidu_link

    def __str__(self):
        return f"LocationEntry( name1={self.name1}, lat_long={self.lat_long}, amap_id={self.amap_id}, address={self.address}, keyword2_count={self.keyword2_count}, name2={self.name2}, amap_link={self.amap_link}, baidu_link={self.baidu_link})"

    def to_dict(self):
        return {
            "name1": self.name1,
            "lat_long": self.lat_long,
            "amap_id": self.amap_id,
            "address": self.address,
            "keyword2_count": self.keyword2_count,
            "name2": self.name2,
            "amap_link": self.amap_link,
            "baidu_link": self.baidu_link
        }