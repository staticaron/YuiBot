query = '''

    query($search : String){
        Character(search :$search, sort:SEARCH_MATCH){
            id
            name{
                full
                native
                alternative
            }
            image{
                medium
            }
            description(asHtml : false)
            gender
            dateOfBirth{
                day
                month
                year
            }
            media(sort:POPULARITY_DESC){
                nodes{
                    title{
                        english
                        romaji
                    }
                    siteUrl
                }
            }
            age
            bloodType
            siteUrl
            favourites
        }
    }
'''