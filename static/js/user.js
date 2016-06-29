var UserProfile = React.createClass({
    formatDate: function(datetime) {
        var monthNames = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ];

        var date = new Date(datetime);
        return monthNames[date.getMonth()] + ", " + date.getFullYear();
    },
    render: function() {
        return (
            <div className="item">
                <div className="ui circular small image">
                    <img src={"https://avatars0.githubusercontent.com/u/"+this.props.student.githubID+"?v=3&s=300"} />
                </div>
                <div className="content">
                    <h1 className="ui header">{ this.props.student.name }</h1>
                    <div className="meta">
                        <h3 className="ui header">{ this.props.student.school.name }</h3>
                    </div>
                    <div className="description">
                        <h3 className="ui header"><a href={"https://github.com/"+this.props.student.username+"/"}>
                            { "@" + this.props.student.username }
                        </a></h3>
                    </div>
                    <div className="extra">
                        Joined { this.formatDate(this.props.student.joinDate) }
                    </div>
                </div>
            </div>
        );
    }
});

var UserTables = React.createClass({
    render: function() {
        var seasons = this.props.seasons;
        return (
            <div>
                { Object.keys(seasons).map(function(key,i){
                    return (
                        <div key={i}>
                        { (i!=0)?<br />:<div></div> /* god I love react */ }
                        <div className="ui horizontal divider">
                            {key}
                        </div>
                        <table className="ui table unstackable">
                            <thead><tr>
                                <th>Problem</th>
                                <th>Score</th>
                                <th>School Rank</th>
                                <th>Overall Rank</th>
                            </tr></thead>
                            <tbody>
                                { seasons[key].map(function(problem,i){
                                    return (
                                        <tr key={i}>
                                        <td><a href={"/problem/"+problem.key}>{ problem.problem }</a></td>
                                        <td>{ problem.score }</td>
                                        <td>{ problem.schoolRank }</td>
                                        <td>{ problem.rank }</td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                        </div>
                    );
                })}
            </div>
        );
    }
});


var dummyStudent = {
    id: 3, githubID: 7736334, name: "Henry Wildermuth",
    school:{id: "HM", name: "Horace Mann"}, compositeScore: 22,
    username: "FlyingGraysons", joinDate: "2015-03-25", history: {
        "Season 0": [
            { problem: "Steiner Tree", key: "steiner-tree", score: 4387, rank: "3/12", schoolRank: "3/12" },
            { problem: "Tron", key: "tron", score: 42, rank: "5/31", schoolRank: "3/8" },
            { problem: "Roommate Problem", key: "roommate", score: 6430, rank: "5/20", schoolRank: "2/5" },
            { problem: "Traveling Salesman Problem", key: "traveling-salesman", score: 583920, rank: "3/12", schoolRank: "1/3" }
        ],
        "Season 1": [
            { problem: "Robot Localization", key: "localization", score: 18, rank: "1/42", schoolRank: "1/12" },
            { problem: "Cryptography", key: "roommate", score: 28, rank: "2/61", schoolRank: "1/10" },
            { problem: "Turing Test", key: "turing-test", score: 60, rank: "4/67", schoolRank: "2/11" }
        ]
    }
}

ReactDOM.render(
    <UserProfile student={dummyStudent} />,
    document.getElementById('userBox')
);

ReactDOM.render(
    <UserTables seasons={dummyStudent.history} />,
    document.getElementById('seasonsBox')
);
