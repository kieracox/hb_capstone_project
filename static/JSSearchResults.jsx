
function JobSeekerSearchResults() {
    const [roles, setRoles] = React.useState([]);
    const [showDetails, setShowDetails] = React.useState({});
    const [connectionRequestResult, setConnectionRequestResult] = React.useState({});
    const [existingConnections, setExistingConnections] = React.useState([]);

    function handleConnect(event, requestedID) {
        event.preventDefault()
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
        {roles.map((role) => (
          <div key={role.id}>
            <p>{role.name}</p>
            <button onClick={() => setShowDetails((prev) => ({ ...prev, [role.id]: !prev[role.id] }))}>
              {showDetails[role.id] ? 'Hide details' : 'Show details'}
            </button>
            {showDetails[role.id] && (
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
        ))}
      </React.Fragment>
    );
  }
  

  
  ReactDOM.render(<JobSeekerSearchResults />, document.querySelector("#js_search_results"))