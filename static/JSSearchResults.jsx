function JobSeekerSearchResults() {
  const [roles, setRoles] = React.useState([]);
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
      console.log("search params", searchParams)
      const paramsDict = JSON.parse(searchParams)
      const queryString = new URLSearchParams(paramsDict).toString();
      fetch(`/search/results/js?${queryString}`)
        .then(response => response.json())
        .then(data => {
          setRoles(data.roles);
          setExistingConnections(data.connections)
        });
    }, []);
  
  if (roles.length === 0) {
      return <p>Your search returned no results.</p>;
    }
  return (
    <React.Fragment>
      <div className="container">
      {roles.map((role) => (
        <div key={role.id} className="search-result">
          <h6>{role.name}</h6>
          <button className="btn btn-secondary rounded focus-state" onClick={() => setShowDetails((prev) => ({ ...prev, [role.id]: !prev[role.id] }))}>
            {showDetails[role.id] ? 'Hide details' : 'Show details'}
          </button>
          {showDetails[role.id] && (
            <div className="details">
              <ul className="list-group" id="search-results-list">
                <li className="list-group-item">Role Type: {role.role_type}</li>
                <li className="list-group-item">Job Description: <a href={role.jd_url}>View it here</a></li>
                <li className="list-group-item">Min YOE: {role.min_yoe}</li>
                <li className="list-group-item">Level: {role.level}</li>
                <li className="list-group-item">Location: {role.location}</li>
                <li className="list-group-item">Min Salary: {role.salary}</li>
                <li className="list-group-item">Remote: {role.remote}</li>
                <li className="list-group-item">Sponsorship Provided: {role.sponsorship_provided}</li>
                <li className="list-group-item">
                  Recruiter for this role: {role.recruiter.fname} {role.recruiter.lname}
                </li>
                <li className="list-group-item">
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
               <input type="text" className="form-control form-control-rounded form-control-sm focus-state" id={`connect_message_${role.recruiter.id}`} placeholder="Optional: Enter a message" />
               <button className="btn btn-secondary rounded show_edit focus-state" id={`id_${role.recruiter.id}`} onClick={(event) => handleConnect(event, role.recruiter.id)}>Send Connection Request</button>
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
      ))}
      </div>
    </React.Fragment>
  );
}



ReactDOM.render(<JobSeekerSearchResults />, document.querySelector("#js_search_results"))