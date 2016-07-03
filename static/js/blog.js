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

$.get('/tempData/blogentries.json', function (result) {
    ReactDOM.render(
        <Blog pages={2} page={1} entries={result} />,
        document.getElementById('blogBox')
    );
});
