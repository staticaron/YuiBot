anime_query = '''
        query ($search : String) { 
            Media (search:$search, type: ANIME, sort:SEARCH_MATCH) { 
                id
                title { 
                    romaji
                    english
                    native
                }
                description(asHtml: false)
                isAdult
                trailer{
                    id
                    site
                }
                siteUrl
                genres
                episodes
                duration
                status
                coverImage {
                    large
                }
                startDate{
                    day
                    month
                    year
                }
                averageScore
                meanScore
                favourites
                format
                studios{
                    nodes{
                        name
                        siteUrl
                    }
                }
            }
        }
    '''

manga_query = """
    query ($search : String) { 
    Media (search:$search, type: MANGA, sort:SEARCH_MATCH) { 
        id
        title {
            romaji
            english
            native
        }
        description(asHtml: false)
        isAdult
        trailer{
            id
            site
        }
        siteUrl
        genres
        chapters
        volumes
        status
        coverImage {
            large
        }
        startDate{
            day
            month
            year
        }
        averageScore
        meanScore
        favourites
        format
        studios(sort:SEARCH_MATCH){
            nodes{
                name
                siteUrl
            }
        }
    }
    }
"""

character_query = """



"""