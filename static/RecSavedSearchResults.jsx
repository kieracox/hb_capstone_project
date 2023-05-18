function RecruiterSearchResults() {
    const [candidates, setCandidates] = React.useState([]);
    const [showDetails, setShowDetails] = React.useState({});
    const [connectionRequestResult, setConnectionRequestResult] = React.useState({});
    const [existingConnections, setExistingConnections] = React.useState([]);
    const [connectMessage, setConnectMessage] = React.useState("");
    
    function handleConnect(event, requestedID) {
      event.preventDefault()
      const requestorID = document.querySelector('#user_id').value;
      const requestedIDValue = document.querySelector(`#rqst_id_${requestedID}`).value
      const connectMessage = document.querySelector(`#connect_message_${requestedID}`).value;
      const formData = {'requested_user': requestedIDValue, 'requesting_user': requestorID, 'connect_message': connectMessage};
      console.log(`requestor ID: ${requestorID}, requested ID: ${requestedIDValue}, formData: ${formData}`)
    
      fetch('/send_connect', {
        method: 'POST',
        body: JSON.stringify(formData),
          headers: {
            'Content-Type': 'application/json'
      }
    })
        .then((response) => response.json())
        .then((data) => {
          console.log('fetch data:', JSON.stringify(data))
          if (data.success) {
            setConnectionRequestResult((prev) => ({ ...prev, [requestedID]: 'success' }));
          } else {
            setConnectionRequestResult((prev) => ({ ...prev, [requestedID]: 'failure' }));
          }
        })
    };

    React.useEffect(() => {
      const searchParams = document.querySelector('#search_params').value;
        const paramsDict = JSON.parse(searchParams)
        const queryString = new URLSearchParams(paramsDict).toString();
        fetch(`/search/results/rec?${queryString}`)
        .then(response => response.json())
        .then(data => { 
          setCandidates(data.candidates);
          setExistingConnections(data.connections);
        })
        

    }, []);

    if (candidates.length === 0) {
        return <p>Your search returned no results.</p>;
      }
      return (
        <React.Fragment>
            {candidates.map((candidate) => (
                <SearchResult
                key={candidate.id}
                candidate={candidate}
                showDetails={showDetails[candidate.id]}
                setShowDetails={setShowDetails}
                existingConnections={existingConnections}
                handleConnect={handleConnect}
                connectionRequestResult={connectionRequestResult}
          />
            ))}
        </React.Fragment>
      );
        }

        function SearchResult({candidate, showDetails, setShowDetails, existingConnections, handleConnect, connectionRequestResult}) {
            return (
              <div className="container">
                <div key={candidate.id} className="search-result">
                <h6>{candidate.fname}{candidate.lname}</h6>
                <button className="btn btn-secondary rounded focus-state" onClick={() => setShowDetails((prev) => ({ ...prev, [candidate.id]: !prev[candidate.id] }))}>
              {showDetails ? 'Hide details' : 'Show details'}
            </button>
            {showDetails && (
                <div className="details">
                    <ul className="list-group" id="search-results-list">
                        <li className="list-group-item">Role Types:
                        <span className="profile_details" id={`cand_roles_${candidate.id}`}>
                            {candidate.role_types.map((role_type) => (
                                <React.Fragment key={role_type.id}>
                                    {role_type.role_type}
                                </React.Fragment>
                            ))}
                        </span>
                        </li>
                        <li className="list-group-item">YOE: {candidate.yoe}</li>
                        <li className="list-group-item">
                            Skills:
                            <span className="profile_details" id={`cand_skills_${candidate.id}`}>
                                {candidate.skills.map((skill) => (
                                    <React.Fragment key={skill.id}>
                                        {skill.skill_name}
                                    </React.Fragment>
                                ))}
                            </span>
                        </li>
                        <li className="list-group-item">Location: {candidate.location}</li>
                        <li className="list-group-item">Min Salary: {candidate.salary}</li>
                        <li className="list-group-item">Remote Only: {candidate.remote_only}</li>
                        <li className="list-group-item">Sponsorship Needed: {candidate.sponsorship_needed}</li>
                        <li className="list-group-item">Linkedin: <a href={`https://${candidate.linkedin}`}>{candidate.linkedin}</a></li>
                        <li className="list-group-item">Github: <a href={`https://${candidate.github}`}>{candidate.github}</a></li>
                        <li className="list-group-item">Resume: <a href={candidate.resume_url}>View it here.</a></li>
                    </ul>
                    {existingConnections.some((connection) => connection.id === candidate.id) ? (
                    <p>You are already connected with this user.</p>
                ) : (
                <div>
                 <p>Want to connect with this candidate?</p>
                 <input type="hidden" id={`rqst_id_${candidate.id}`} value={candidate.id}/>
                 <input className="form-control form-control-rounded form-control-sm focus-state" type="text" id={`connect_message_${role.candidate.id}`} placeholder="Optional: Enter a message" />
                 <button id={`id_${candidate.id}`} className="btn btn-secondary rounded show_edit focus-state" onClick={(event) => handleConnect(event, candidate.id)}>Send Connection Request</button>
                {connectionRequestResult[candidate.id] === 'success' && (
                  <p id={`success_${candidate.id}`}>Connection request sent!</p>
                )}
                {connectionRequestResult[candidate.id] === 'failure' && (
                <p id={`failure_${candidate.id}`}>Request failed: you already have a pending request for this user.</p>
                )}
                </div>
                )}
                </div>
            )}

            </div>
            </div>
            );
        }
        ReactDOM.render(<RecruiterSearchResults/>, document.querySelector("#rec_saved_search_results"));