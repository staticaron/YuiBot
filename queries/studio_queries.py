studio_query = """
    query($search : String){
        Studio(search : $search){
            id
            name
            isAnimationStudio
            media(sort : POPULARITY_DESC){
                nodes{
                    title{
                        english
                        romaji
                    }
                    siteUrl
                    format
                    status
                }
            }
            siteUrl
            favourites
        }
    }    
"""
