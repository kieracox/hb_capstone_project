function JobSeekerSearchResults() {
    const [roles, setRoles] = React.useState([]);
    const [showDetails, setShowDetails] = React.useState({});
    const [connectionRequestResult, setConnectionRequestResult] = React.useState({});
    const [existingConnections, setExistingConnections] = React.useState([]);
    const [connectMessage, setConnectMessage] = React.useState("");
  
    function handleConnect(event, requestedID) {
      event.preventDefault();
      const requestorID = document.querySelector('#user_id').value;
      const requestedIDValue = document.querySelector(`#rqst_id_${requestedID}`).value;
      const connectMessage = document.querySelector(`#connect_message_${requestedID}`).value;
      const formData = {'requested_user': requestedIDValue, 'requesting_user': requestorID, 'connect_message': connectMessage};
  
      fetch('/send_connect', {
        method: 'POST',
        body: JSON.stringify(formData),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            setConnectionRequestResult((prev) => ({ ...prev, [requestedID]: 'success' }));
          } else {
            setConnectionRequestResult((prev) => ({ ...prev, [requestedID]: 'failure' }));
          }
        });
    }
  
    React.useEffect(() => {
      const searchParams = document.querySelector('#search_params').value;
      const paramsDict = JSON.parse(searchParams);
      const queryString = new URLSearchParams(paramsDict).toString();
      console.log("params", searchParams)
      console.log("query string", queryString)
      fetch(`/search/results/js?${queryString}`)
        .then(response => response.json())
        .then(data => {
          setRoles(data.roles);
          setExistingConnections(data.connections);
        });
    }, []);
  
    if (roles.length === 0) {
      return <p>Your search returned no results.</p>;
    }
  
    return (
      <React.Fragment>
        {roles.map((role) => (
          <SearchResult
            key={role.id}
            role={role}
            showDetails={showDetails[role.id]}
            setShowDetails={setShowDetails}
            existingConnections={existingConnections}
            handleConnect={handleConnect}
            connectionRequestResult={connectionRequestResult}
          />
        ))}
      </React.Fragment>
    );
  }
  
  function SearchResult({ role, showDetails, setShowDetails, existingConnections, handleConnect, connectionRequestResult }) {
    return (
      <div key={role.id}>
        <p>{role.name}</p>
        <button onClick={() => setShowDetails((prev) => ({ ...prev, [role.id]: !prev[role.id] }))}>
          {showDetails ? 'Hide details' : 'Show details'}
        </button>
        {showDetails && (
          <div className="details">
            <ul>
              <li>Role Type: {role.role_type}</li>
              <li>Job Description: <a href={role.jd_url}>View it here</a></li>
              <li>Min YOE: {role.min_yoe}</li>
              <li>Level: {role.level}</li>
              <li>Location: {role.location}</li>
              <li>Min Salary: {role.salary}</li>
              <li>Remote: {role.remote}</li>
              <li>Sponsorship Provided: {role.sponsorship_provided}</li>
              <li>
                Recruiter for this role: {role.recruiter.fname} {role.recruiter.lname}
              </li>
              <li>
                Recruiter's Linkedin:{' '}
                <a href={`https://${role.recruiter.linkedin}`}>{role.recruiter.linkedin}</a>
                </li>
          </ul>
          {existingConnections.some((connection) => connection.id === role.recruiter.id) ? (
            <p>You are already connected with this user.</p>
          ) : (
            <div>
              <p>Want to connect with the recruiter for this role?</p>
              <input type="hidden" id={`rqst_id_${role.recruiter.id}`} value={role.recruiter.id}></input>
              <input type="text" id={`connect_message_${role.recruiter.id}`} placeholder="Optional: Enter a message" />
              <button id={`id_${role.recruiter.id}`} onClick={(event) => handleConnect(event, role.recruiter.id)}>Send Connection Request</button>
              {connectionRequestResult[role.recruiter.id] === 'success' && (
                <p id={`success_${role.recruiter.id}`}>Connection request sent!</p>
              )}
              {connectionRequestResult[role.recruiter.id] === 'failure' && (
                <p id={`failure_${role.recruiter.id}`}>Request failed: you already have a pending request for this user.</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

ReactDOM.render(<JobSeekerSearchResults />, document.querySelector("#js_saved_search_results"));

                
  