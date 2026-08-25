import aiohttp

async def get_steam_tr_deals():
    url = "https://store.steampowered.com/api/featuredcategories/?cc=tr&l=turkish"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                deals = data.get("specials", {}).get("items", [])
                
                indirimli_oyunlar = []
                for game in deals:
                    original_price = game["original_price"] / 100
                    final_price = game["final_price"] / 100
                    discount_percent = game["discount_percent"]
                    game_id = game["id"]
                    image_url = game["header_image"]
                    
                    if discount_percent > 0 and original_price > 0:
                        indirimli_oyunlar.append({
                            "name": game["name"],
                            "original_price": f"${original_price:.2f}",
                            "final_price": f"${final_price:.2f}",
                            "discount": f"-{discount_percent}%",                        
                            "url": f"https://store.steampowered.com/app/{game_id}/",
                            "image_url": image_url
                        })
                return indirimli_oyunlar
            
            return []