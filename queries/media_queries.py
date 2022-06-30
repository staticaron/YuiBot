anime_query = '''
        query ($search : String) { 
        Media (search:$search, type: ANIME) { 
            id
            title { 
                romaji
                english
                native
            }
            description(asHtml: true)
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
            seasonInt
        }
        }
    '''

manga_query = """
    query ($search : String) { 
    Media (search:$search, type: MANGA) { 
        id
        title {
            romaji
            english
            native
        }
        description(asHtml: true)
        isAdult
        trailer
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
        seasonInt
    }
    }
"""