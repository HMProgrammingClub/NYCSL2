var QualifiedLeaderboard = React.createClass({
    render: function() {
        return (
            <table className="ui very basic celled table fluid">
                <thead><tr>
                    <th>Student</th>
                    <th>Composite Score</th>
                </tr></thead>
                <tbody>
                    {this.props.students.map(function(student) {
                        return (
                            <tr key={ student.id }>
                                <td>
                                    <h4 className="ui image header">
                                        <img src={"https://avatars0.githubusercontent.com/u/" + student.githubID + "?v=3&s=50"} className="ui mini rounded image" />
                                        <div className="content">
                                            { student.name }
                                            <div className="sub header">{ student.school.name }</div>
                                        </div>
                                    </h4>
                                </td>
                                <td>{ student.compositeScore }</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        );
    }
});

QualifiedData = [
    { id: 3, githubID: 7736334, name: "Henry Wildermuth", school:{id: "HM", name: "Horace Mann" }, compositeScore: 22},
    { id: 3, githubID: 7736334, name: "Joshua Gruenstein", school:{id: "HM", name: "Horace Mann" }, compositeScore: 32}
]

ReactDOM.render(
    <QualifiedLeaderboard students={QualifiedData} />,
    document.getElementById('qualifiedBox')
);
