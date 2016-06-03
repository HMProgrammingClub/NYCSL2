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
            <tr class={'playerRow' + user.id}>
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

var data = [
    {user: {id: 1, username: "joshuagruenstein", name: "Joshua Gruenstein", school: "Horace Mann"}, rank: 1, score: 44},
    {user: {id: 2, username: "truell20", name: "Michael Truell", school: "Horace Mann"}, rank: 2, score: 33}
]

ReactDOM.render(
    <Leaderboard data={data} />,
    document.getElementById('leaderBoard')
);
