
// dynamically update upcoming CTFs section using JSON file 
// retrieved from ctftime's rss feed.

const rss = import('./upcomingCTFsRSS.json', {
    assert: {
        type: 'json'
    }
});


//loading rss 
rss.then( r => 
    r.default.forEach(data => { 

        var div = document.createElement('div');
        div.className = 'media-element';

        var header = document.createElement('p');
        header.className = 'my-3 waviy';

        var head_url = document.createElement('a');
        head_url.id = "links"
        head_url.className = "linkss"
        head_url.href = data.url

        const title_array = data.title.split(" ")
        for(let i = 0; i < title_array.length; i++) {
            var span = document.createElement('span');
            span.style = `--i:${i+1}`;
            span.appendChild(document.createTextNode(`${title_array[i]} `));
            head_url.appendChild(span);
        }

        header.appendChild(head_url);


        var url = document.createElement('a');
        url.href = data.url
        url.target = '_blank'

        var img = document.createElement('img');
        img.src = data.logo_path;
        img.alt = `${data.title}'s logo`;
        url.appendChild(img);

        var p = document.createElement('p');
        p.className = "text-muted"
        p.appendChild(document.createTextNode(data.description));

        div.appendChild(header);
        div.appendChild(url);
        div.appendChild(p);

        var element = document.getElementById('media-scroller');
        element.appendChild(div);
})
);

