var Blog = React.createClass({
    navigate: function(interval) {
        alert(interval)
    },
    navBtn: function(forwards) {
        return (
            <div className={"ui " + (forwards?"right":"left") + " floated segment basic"}>
                <button className="circular ui button" onClick={()=>this.navigate(forwards?1:-1)}>
                    {forwards?"next":""}<i className={"chevron " + (forwards?"right":"left") + " icon"}></i>{forwards?"":"back"}
                </button>
            </div>
        );
    },
    render: function() {
        return (
            <div>
                {this.props.entries.map(function(entry) {
                    return (
                        <div className="blogEntry" key={entry.id}>
                            <h1 className="header">{entry.title}</h1>
                            <h3 className="author">by <a href={"/student/" + entry.author.username}>{entry.author.name}</a></h3>
                            <h4 className="date">{entry.date}</h4>
                            <div className="content" dangerouslySetInnerHTML={{__html: entry.body}}></div>
                        </div>
                    );
                })} { this.props.page>1?this.navBtn(false):""} { this.props.page<this.props.pages?this.navBtn(true):""}
            </div>
        );
    }
});

var BlogEntries = [
    {
        id: 1,
        url: "tron-post-mortem",
        title: "Tron: A Post-Mortem",
        author: {username: "joshuagruenstein", name: "Joshua Gruenstein"},
        date: "June 21, 2016",
        body: "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam iaculis nulla eget lacus lacinia, et blandit dui hendrerit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nam sit amet sem sed nisi scelerisque hendrerit. Fusce laoreet erat ex, vitae maximus lorem commodo dictum. Etiam pretium quis diam quis rutrum. Etiam laoreet commodo gravida. Suspendisse dapibus lorem quis dolor euismod laoreet. Integer dignissim ligula eu rutrum lacinia. Sed facilisis maximus risus, rutrum viverra risus maximus sed. Quisque congue nulla eros, eu facilisis lorem consectetur sit amet. Pellentesque dolor nulla, tincidunt vel arcu vitae, porta tempus ex. Vivamus tempor dolor in ligula feugiat porta. Nullam at suscipit nibh. Quisque placerat ornare nulla eu mattis. Maecenas eu velit mollis, posuere quam quis, lacinia magna.</p><p>Fusce varius sed lacus eget tristique. Donec sodales, lorem non auctor gravida, ligula lorem laoreet sem, at posuere justo turpis varius felis. Suspendisse lobortis, nibh at blandit rhoncus, nisi velit vulputate dolor, ut aliquam mi nisl et enim. Donec quis ipsum nunc. Quisque felis felis, egestas sit amet magna sit amet, fringilla malesuada lorem. Quisque sit amet sapien interdum, malesuada metus nec, tristique purus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque justo dolor, ullamcorper ac urna id, ornare blandit quam. Praesent eu ultricies nisi. Curabitur sollicitudin sed nibh et gravida. Phasellus magna metus, tincidunt vel diam at, suscipit iaculis nisl. Duis non nulla a tellus molestie pharetra. Curabitur vulputate tortor purus, ac interdum eros placerat vitae. Fusce faucibus gravida nisl pulvinar tempor. Proin at leo dictum, auctor tortor non, auctor ex. Maecenas lacinia interdum urna, quis tincidunt elit aliquam eget.</p>"
    }
];

ReactDOM.render(
    <Blog pages={2} page={1} entries={BlogEntries} />,
    document.getElementById('blogBox')
);
