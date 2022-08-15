anime_query = """
    mutation($id:Int!){
        ToggleFavourite(animeId:$id){
            anime {
                nodes {
                    id
                }
            }
        }
    }
"""

manga_query = """
    mutation($id:Int!){
        ToggleFavourite(mangaId:$id){
            manga {
                nodes {
                    id
                }
            }
        }
    }
"""

character_query = """
    mutation($id:Int!){
        ToggleFavourite(characterId:$id){
            characters {
                nodes {
                    id
                }
            }
        }
    }
"""

anime_list_query = """
    query($userID:Int!){
        User(id:$userID){
            favourites{
            anime{
                nodes{
                title{
                    english
                    romaji
                }
                siteUrl
                }
            }
            }
        }
    }
"""

manga_list_query = """
    query($userID:Int!){
        User(id:$userID){
            favourites{
            manga{
                nodes{
                title{
                    english
                    romaji
                }
                siteUrl
                }
            }
            }
        }
    }
"""

character_list_query = """
    query($userID:Int!){
        User(id:$userID){
            favourites{
                characters{
                    nodes{
                        name{
                            full
                            native
                        }
                        siteUrl
                    }
                }
            }
        }
    }
"""