var Feed = React.createClass({
    render: function() {
        return (
            <div className={"ui flowing popup gamePopup " + this.props.id}>
                <div className="ui feed">
                    {this.props.events.map(function(feedEvent, i) {
                        return (
                            <div className="event" key={i}>
                                <div className="label">
                                    <i className={feedEvent.type === "upload" ? "file archive outline icon" : "game icon"}></i>
                                </div>
                                <div className="content summary">
                                    <div className="summary">
                                        { feedEvent.event }
                                        <div className="date">
                                            { timeSince(feedEvent.time) + " ago" }
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }
});


var Leaderboard = React.createClass({
    componentDidMount: function() {
        // link rows and popups
        var rows = document.querySelectorAll(".playerRow");
        for (var i=0; i<rows.length; i++) {
            var className = rows[i].className;
            className = className.substr(className.indexOf(' ')+1);
            $('.playerRow.' + className).popup({
                popup:$('.gamePopup.' + className),
                hoverable:true,
                position : 'bottom right'
            });
        }
    },
    render: function() {
        return (
            <div className="leaderboard">
                <table className="ui table unstackable">
                    <thead><tr>
                        <th>Rank</th>
                        <th>Name</th>
                        <th>School</th>
                        <th>Score</th>
                    </tr></thead>
                    <tbody>
                        {this.props.rows.map(function(row) {
                            return (
                                <tr className={'playerRow ' +row.user.id} key={row.rank}>
                                    <td><b>{row.rank}</b></td>
                                    <td><a href={'/user/' + row.user.username}>{row.user.name}</a></td>
                                    <td>{row.user.school}</td>
                                    <td>{row.score}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
                {this.props.feeds.map(function(feed) {
                    return <Feed events={feed.events} id={feed.id} key={feed.id} />
                })}
            </div>
        );
    }
});

var Jumbo = React.createClass({
    render: function() {
        return (
            <div className="row">
                <div className="row column">
                    <div className="ui huge message page grid">
                        <h1 className="ui huge header">{this.props.game}</h1>
                        <p>{this.props.desc}
                        <br />
                        {this.props.links.map(function(link, i) {
                            return <a className="ui blue basic button" style={{marginTop:"10px"}} href={link.url} key={i}>{link.txt}</a>
                        })}
                        </p>
                    </div>
                </div>
            </div>
        );
    }
});

var jumboData = {game:"Steiner Tree", desc:"Find the shortest interconnection for a given set of points.", links:[
    {url:"/blog/steiner-tree",txt:"Learn More"},
    {url:"/blog/steiner-tree-tutorial",txt:"Tutorials"}
]}

var leaderData = [
    {user: {id: 1, username: "joshuagruenstein", name: "Joshua Gruenstein", school: "Horace Mann"}, rank: 1, score: 44},
    {user: {id: 2, username: "truell20", name: "Michael Truell", school: "Horace Mann"}, rank: 2, score: 33}
];

var feedData = [
    {id: 1, events: [{type: "upload", event: "New bot uploaded", time: new Date(new Date().getTime()-300000)},
                     {type: "game", event: "Won against Henry Hunt", time: new Date(new Date().getTime()-600000)}]},
    {id: 2, events: [{type: "upload", event: "New bot uploaded", time: new Date(new Date().getTime()-300000)},
                     {type: "game", event: "Won against Joshua Gruenstein", time: new Date(new Date().getTime()-600000)}]}
];

ReactDOM.render(
    <Leaderboard rows={leaderData} feeds={feedData} />,
    document.getElementById('leaderBoard')
);

ReactDOM.render(
    <Jumbo game={jumboData.game} desc={jumboData.desc} links={jumboData.links} />,
    document.getElementById('jumboBox')
);
