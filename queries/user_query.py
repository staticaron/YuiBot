user_query = """
    query($id:Int!){
        User(id:$id){
            name
            siteUrl
            avatar{
                medium
            }
            favourites(page:0){
                anime(page:0, perPage:3) {
                    nodes{
                        title{
                            english
                            romaji
                        }
                        siteUrl
                    }
                }
                manga(page:0, perPage:3) {
                    nodes{
                        title{
                            english
                            romaji
                        }
                        siteUrl
                    }
                }
                characters(page:0, perPage:3) {
                    nodes{
                        name {
                            full
                        }
                        siteUrl
                    }
                }
            }
            statistics{
                anime{
                    count
                    meanScore
                    standardDeviation
                    episodesWatched
                    genres(limit:3, sort:COUNT_DESC){
                        genre
                    }
                }
                manga{
                    count
                    meanScore
                    standardDeviation
                    chaptersRead
                    genres(limit:3, sort:COUNT_DESC){
                            genre
                    }
                }
            }
        }
        Page{
            pageInfo{
                total
            }
            followers(userId:$id){
                name
            }
        }
    }
"""

anime_stats_query = """
    query($userID:Int!){
        User(id:$userID) {
            name
            siteUrl
            avatar{
                medium
            }
            statistics {
                anime {
                    count
                    meanScore
                    episodesWatched
                    minutesWatched
                    standardDeviation
                }
            }
        }
    }

"""

manga_stats_query = """
    query($userID:Int!){
        User(id:$userID) {
            name
            siteUrl
            avatar{
                medium
            }
            statistics {
                manga {
                    count
                    meanScore
                    chaptersRead
                    volumesRead
                }
            }
        }
    }
"""