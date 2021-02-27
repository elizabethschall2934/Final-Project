function displayData(data) {
    var dataTable = $('#table_data').DataTable({
        fixedHeader: {
            header: true,
            footer: true
        },
        keys: true,
        data: data,
        columns: [
            { data: 'type'},
            { data: 'breeds.primary'},
            { data: 'age'},
            { data: 'gender'},
            { data: 'size'},
            { data: 'colors.primary'},
            { data: 'tags'}
        ],
        searchPanes: {
            columns: [0,1,3,4,5,6,7],
            layout: 'columns-5',
            cascadePanes: true
        },
        dom: 'Plfrtip'
    });

    $('#table_data tbody').on('click', 'tr', function () {
        var popData = dataTable.row(this).data();
        console.log(popData.description)
        var items = [];
        if (popData.photos.length === 0) {
            items = {src: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png',
                    pet_name: popData.name,
                    pet_url: popData.url,
                    pet_desc: popData.description}
        } else {
            var i;
            for (i = 0; i < popData.photos.length; i++){
                items.push({src: `${popData.photos[i].full}`,
                            pet_name: popData.name,
                            pet_url: popData.url,
                            pet_desc: popData.description})
            }
        }
        $.magnificPopup.open({
            items: items,
            gallery: {
                enabled: true
              },
            type: 'image',
            image: {
                titleSrc: function(item) {
                    return `<p id="gallery-image-title">Name: ${item.data.pet_name} | <a href="${item.data.pet_url}" target="_blank" style="color:white;">Click to Petfinder</a></p>
                            <p id="gallery-image-description"><br>${item.data.pet_desc}</p>`;
                }
            }
        });
    } );
};