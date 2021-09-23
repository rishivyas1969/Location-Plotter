import folium


def map(lst=None):

    if type(lst) == None:
        return None
    sum_lat=0
    sum_long=0
    for i in lst:
        sum_lat+=i[1]
        sum_long+=i[2]

    avg_lat=sum_lat/len(lst)
    avg_long=sum_long/len(lst)

    map = folium.Map(location=[avg_lat, avg_long], zoom_start=3, tiles="CartoDB dark_matter")

    fgv = folium.FeatureGroup("Plots")

    for i in range(len(lst)):
        pop = lst[i][0]

        icon = folium.Icon(color='orange', icon='map-marker-alt', prefix='fa')

        fgv.add_child(folium.Marker(
            location=[lst[i][1], lst[i][2]],
            popup=pop,
            icon=icon))

    map.add_child(fgv)

    map.add_child(folium.LayerControl())
    return map.get_root().render()