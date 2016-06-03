function linkPopups() {
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
}

var PlayerRow = React.createClass({
    render: function() {
        var user = this.props.data.user;
        return (
            <tr className={'playerRow ' + user.id}>
                <td><b>{this.props.data.rank}</b></td>
                <td><a href={'/user/' + user.username}>{user.name}</a></td>
                <td>{user.school}</td>
                <td>{this.props.data.score}</td>
            </tr>
        );
    }
});

var Leaderboard = React.createClass({
    render: function() {
        return (
            <table className="ui table unstackable">
                <thead><tr>
                    <th>Rank</th>
                    <th>Name</th>
                    <th>School</th>
                    <th>Score</th>
                </tr></thead>
                <tbody>
                    {this.props.data.map(function(playerRow) {
                        return <PlayerRow data={playerRow} />
                    })}
                </tbody>
            </table>
        );
    }
});

var FeedEvent = React.createClass({
    render: function() {
        return (
            <div className="event">
                <div className="label">
                    <i className={this.props.data.type === "upload" ? "file archive outline icon" : "game icon"}></i>
                </div>
                <div className="content summary">
                    <div className="summary">
                        { this.props.data.event }
                        <div className="date">
                            { timeSince(this.props.data.time) + " ago" }
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

var Feed = React.createClass({
    render: function() {
        return (
            <div className={"ui flowing popup gamePopup " + this.props.data.id}>
                <div className="ui feed">
                    {this.props.data.events.map(function(feedEvent) {
                        return <FeedEvent data={feedEvent} />
                    })}
                </div>
            </div>
        );
    }
});

var Feeds = React.createClass({
    render: function() {
        return (
            <div>
                {this.props.data.map(function(feed) {
                        return <Feed data={feed} />
                })}
            </div>
        );
    }
});


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
    <Leaderboard data={leaderData} />,
    document.getElementById('leaderBoard')
);

ReactDOM.render(
    <Feeds data={feedData} />,
    document.getElementById('feedsBox')
);

linkPopups();
