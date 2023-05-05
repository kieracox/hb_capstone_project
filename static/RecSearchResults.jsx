function RecruiterSearchResults() {
    const [candidates, setCandidates] = React.useState([]);
    const [showDetails, setShowDetails] = React.useState({});
    const [connectionRequestResult, setConnectionRequestResult] = React.useState({});
    const [existingConnections, setExistingConnections] = React.useState([]);

    function handleConnect(requestedID) {
      const requestorID = document.querySelector('#user_id').value;
      const requestedIDValue = document.querySelector(`#rqst_id_${requestedID}`).value
      const formData = {'requested_user': requestedIDValue, 'requesting_user': requestorID};
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
        console.log(searchParams)
        const paramsDict = JSON.parse(searchParams)
        console.log(paramsDict)
        const queryString = new URLSearchParams(paramsDict).toString();
        fetch(`/search/results/rec?${queryString}`)
        .then(response => response.json())
        .then(data => { setCandidates(data.candidates);
        })
        

    }, []);

    return (
        <React.Fragment>
        {candidates.map((candidate) => (
            <div key={candidate.id}>
                <p>{candidate.fname}{candidate.lname}</p>
                <button onClick={() => setShowDetails((prev) => ({ ...prev, [candidate.id]: !prev[candidate.id] }))}>
              {showDetails[candidate.id] ? 'Hide details' : 'Show details'}
            </button>
            {showDetails[candidate.id] && (
                <div className="details">
                    <ul>
                        <li>Role Types:
                        <span className="profile_details" id={`cand_roles_${candidate.id}`}>
                            {candidate.role_types.map((role_type) => (
                                <React.Fragment key={role_type.id}>
                                    {role_type.role_type}
                                </React.Fragment>
                            ))}
                        </span>
                        </li>
                        <li>YOE: {candidate.yoe}</li>
                        <li>
                            Skills:
                            <span className="profile_details" id={`cand_skills_${candidate.id}`}>
                                {candidate.skills.map((skill) => (
                                    <React.Fragment key={skill.id}>
                                        {skill.skill_name}
                                    </React.Fragment>
                                ))}
                            </span>
                        </li>
                        <li>Location: {candidate.location}</li>
                        <li>Min Salary: {candidate.salary}</li>
                        <li>Remote Only: {candidate.remote_only}</li>
                        <li>Sponsorship Needed: {candidate.sponsorship_needed}</li>
                        <li>Linkedin: <a href={`https://${candidate.linkedin}`}>{candidate.linkedin}</a></li>
                        <li>Github: <a href={`https://${candidate.github}`}>{candidate.github}</a></li>
                        <li>Resume: <a href={candidate.resume_url}>View it here.</a></li>
                    </ul>
                    {existingConnections.includes(candidate.id) ? (
                <p>You are already connected with this user.</p>
                ) : (
                <div>
                 <p>Want to connect with this candidate?</p>
                 <input type="hidden" id={`rqst_id_${candidate.id}`} value={candidate.id}></input>
                 <button id={`id_${candidate.id}`} onClick={() => handleConnect(candidate.id)}>Send Connection Request</button>
                {connectionRequestResult[candidate.id] === 'success' && (
                  <p id={`success_${candidate.id}`}>Connection request sent!</p>
                )}
                {connectionRequestResult[candidate.id] === 'failure' && (
                <p id={`failure_${role.recruiter.id}`}>Request failed: you already have a pending request for this user.</p>
                )}
                </div>
                )}
                </div>
            )}

            </div>
        ))}
        </React.Fragment>
    )
};
  

  ReactDOM.render(<RecruiterSearchResults />, document.querySelector("#rec_search_results"))