from Issue import Issue, IssueStatus
from IssueType import IssueType
from Agent import Agent
from IssueRepository import IssueRepository
from AgentRepository import AgentRepository
from AssignmentStrategy import LeastLoadedAgentStrategy
from IssueFilter import IssueFilter

class IssueManager:
    def __init__(self):
        self.agent_repository = AgentRepository()
        self.issue_repository = IssueRepository()
        self._strategy = LeastLoadedAgentStrategy()

    def _set_strategy(self, strategy):
        self._strategy = strategy

    def createIssue(self, transactionId, issueType, subject, description, email):
        try:
            issue = Issue(transactionId, issueType, subject, description, email)
            self.issue_repository.save(issue)
            return issue.id
        except Exception as err:
            raise err
        
    def addAgent(self, agentId, email, expertise):
        try:
            agent = Agent(agentId, email, expertise)
            self.agent_repository.save(agent)
        except Exception as err:
            raise err

    def assignIssue(self, issueId):
        try:
            issue = self.issue_repository.get(issueId)
            if not issue.is_open():
                raise RuntimeError("Issue is not in OPEN status - cannot assign")
            
            issue_type = issue.get_type()
            agents = self.agent_repository.list()
            agents_with_expertise = []
            for agent in agents:
                if issue_type in agent.get_expertise():
                    agents_with_expertise.append(agent)
            
            assigned_agent = self._strategy.assign(agents_with_expertise)
            if not assigned_agent:
                return
            
            issue.assign(assigned_agent)
            assigned_agent.add_new_issue(issueId)

        except Exception as err:
            raise err

    def resolveIssue(self, issueId):
        try:
            issue = self.issue_repository.get(issueId)
            issue.resolve()
            assigned_agent = self.agent_repository.get(issue.get_assigned_agent())
            assigned_agent.resolve_issue(issueId)
        except Exception as err:
            raise err

    def getIssues(self, filter):
        try:
            issues = self.issue_repository.list()
            filtered_issues = []
            for issue in issues:
                if filter.type and issue.get_type() != filter.type:
                    continue
                if filter.status and issue.get_status() != filter.status:
                    continue
                if filter.email and issue.get_email() != filter.email:
                    continue
                if filter.agent_id and issue.get_assigned_agent() != filter.agent_id:
                    continue
                filtered_issues.append(issue.get_summary())
            return filtered_issues
        
        except Exception as err:
            raise err
            


if __name__ == '__main__':
    manager = IssueManager()

    def assert_equals(expected, actual, message):
        if expected != actual:
            raise AssertionError(f"FAILED: {message} | Expected={expected}, Actual={actual}")
        else:
            print(f"PASSED: {message}")
    
    print("\n--- TEST 1: Add Agents ---")
    manager.addAgent("A1", "agent1@test.com", ["PAYMENT_FAILED", "REFUND"])
    manager.addAgent("A2", "agent2@test.com", ["PAYMENT_FAILED"])
    manager.addAgent("A3", "agent3@test.com", ["KYC"])

    agents = manager.agent_repository.list()
    assert_equals(3, len(agents), "Agents added successfully")

    print("\n--- TEST 2: Create Issues ---")
    i1 = manager.createIssue("T1", "PAYMENT_FAILED", "Payment failed", "desc", "cust1@test.com")
    i2 = manager.createIssue("T2", "PAYMENT_FAILED", "Refund missing", "desc", "cust2@test.com")
    i3 = manager.createIssue("T3", "KYC", "KYC issue", "desc", "cust3@test.com")

    issues = manager.issue_repository.list()
    assert_equals(3, len(issues), "Issues created successfully")

    print("\n--- TEST 3: Assign Issue (Least Loaded Agent) ---")
    manager.assignIssue(i1)

    issue = manager.issue_repository.get(i1)
    assert_equals(IssueStatus.ASSIGNED, issue.get_status(), "Issue status updated after assignment")
    assert_equals("A1", issue.get_assigned_agent(), "Assigned to correct agent")

    print("\n--- TEST 4: Least Loaded Assignment ---")
    manager.assignIssue(i2)

    issue2 = manager.issue_repository.get(i2)
    assert_equals("A2", issue2.get_assigned_agent(), "Assigned to next least-loaded agent")

    print("\n--- TEST 5: Expertise Matching ---")
    manager.assignIssue(i3)

    issue3 = manager.issue_repository.get(i3)
    assert_equals("A3", issue3.get_assigned_agent(), "Assigned to correct expertise agent")

    print("\n--- TEST 6: Assign Already Assigned Issue ---")
    try:
        manager.assignIssue(i1)
        raise AssertionError("FAILED: Should not assign already assigned issue")
    except Exception:
        print("PASSED: Prevented reassignment")

    print("\n--- TEST 7: Resolve Issue ---")
    manager.resolveIssue(i1)

    issue = manager.issue_repository.get(i1)
    assert_equals(IssueStatus.RESOLVED, issue.get_status(), "Issue resolved successfully")

    print("\n--- TEST 8: Resolve Unassigned Issue ---")
    i4 = manager.createIssue("T4", "PAYMENT_FAILED", "Another issue", "desc", "cust4@test.com")

    try:
        manager.resolveIssue(i4)
        raise AssertionError("FAILED: Should not resolve unassigned issue")
    except Exception:
        print("PASSED: Prevented resolving OPEN issue")

    print("\n--- TEST 9: Filter by Status ---")
    open_filter = IssueFilter(status=IssueStatus.OPEN)
    open_issues = manager.getIssues(open_filter)

    assert_equals(1, len(open_issues), "Filtering OPEN issues works")

    print("\n--- TEST 10: Filter by Agent ---")
    agent_filter = IssueFilter(agent_id="A2")
    agent_issues = manager.getIssues(agent_filter)

    assert_equals(1, len(agent_issues), "Filtering by agent works")

    print("\n--- TEST 11: Filter by Issue Type ---")
    type_filter = IssueFilter(type="PAYMENT_FAILED")
    type_issues = manager.getIssues(type_filter)

    assert_equals(True, len(type_issues) >= 2, "Filtering by issue type works")

    print("\n--- TEST 12: Issue Type With No Agent ---")
    i5 = manager.createIssue("T5", "FRAUD", "Fraud complaint", "desc", "cust5@test.com")

    manager.assignIssue(i5)

    issue = manager.issue_repository.get(i5)
    assert_equals(IssueStatus.OPEN, issue.get_status(), "Issue remains OPEN if no expert agent")

    print("\n--- ALL TESTS PASSED ---")