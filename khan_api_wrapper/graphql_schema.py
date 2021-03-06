# QUERIES

simpleCompletionQuery = """query simpleCompletionQuery($assignmentId: String!) {
  coach {
    id
    assignment(id: $assignmentId) {
      contents {
        id
        translatedTitle
        defaultUrlPath
        kind
        __typename
      }
      assignedDate
      dueDate
      id
      itemCompletionStates {
        student {
          id
          kaid
          coachNickname
          profileRoot
          __typename
        }
        state
        completedOn
        bestScore {
          numCorrect
          numAttempted
          __typename
        }
        exerciseAttempts {
          id
          isCompleted
          numAttempted
          numCorrect
          lastAttemptDate
          __typename
        }
        __typename
      }
      studentList {
        id
        name
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

getStudentsList = """query getStudentsList($hasClassId: Boolean!, $classId: String!, $after: Int, $pageSize: Int) {
  coach {
    id
    studentsPage(after: $after, pageSize: $pageSize) @skip(if: $hasClassId) {
      ...StudentField
      __typename
    }
    invitations @skip(if: $hasClassId) {
      ...InvitationsField
      __typename
    }
    coachRequests @skip(if: $hasClassId) {
      ...CoachRequestField
      __typename
    }
    studentLists {
      id
      name
      key
      students @skip(if: $hasClassId) {
        id
        kaid
        __typename
      }
      __typename
    }
    studentList(id: $classId) @include(if: $hasClassId) {
      id
      name
      key
      autoGenerated
      signupCode
      topics {
        id
        key
        iconPath
        __typename
      }
      studentsPage(after: $after, pageSize: $pageSize) {
        ...StudentField
        __typename
      }
      invitations {
        ...InvitationsField
        __typename
      }
      coachRequests {
        ...CoachRequestField
        __typename
      }
      __typename
    }
    schoolAffiliation {
      id
      __typename
    }
    affiliationCountryCode
    __typename
  }
}

fragment CoachRequestField on CoachRequest {
  id
  email: studentIdentifier
  __typename
}

fragment InvitationsField on Invitation {
  id
  email
  accepted
  __typename
}

fragment StudentField on StudentsPage {
  students {
    id
    email
    nickname
    coachNickname
    profileRoot
    username
    __typename
  }
  countStudents
  nextCursor
  __typename
}
"""

quizAndUnitTestAttemptsQuery = """query quizAndUnitTestAttemptsQuery($topicId: String!, $kaid: String) {
  user {
    id
    latestUnitTestAttempts(unitId: $topicId) {
      id
      numAttempted
      numCorrect
      completedDate
      canResume
      isCompleted
      __typename
    }
    latestQuizAttempts(topicId: $topicId) {
      id
      numAttempted
      numCorrect
      completedDate
      canResume
      isCompleted
      positionKey
      __typename
    }
    __typename
  }
}
"""

progressByStudent = """query ProgressByStudent($assignmentFilters: CoachAssignmentFilters, $contentKinds: [LearnableContentKind], $classId: String!, $pageSize: Int, $after: ID) {
  coach {
    id
    studentList(id: $classId) {
      id
      students {
        id
        coachNickname
        __typename
      }
      assignmentsPage(filters: $assignmentFilters, after: $after, pageSize: $pageSize) {
        assignments(contentKinds: $contentKinds) {
          id
          dueDate
          contents {
            id
            translatedTitle
            kind
            defaultUrlPath
            __typename
          }
          itemCompletionStates {
            completedOn
            studentKaid
            bestScore {
              numAttempted
              numCorrect
              __typename
            }
            __typename
          }
          __typename
        }
        pageInfo {
          nextCursor
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

AutoAssignableStudents = """query AutoAssignableStudents($studentListId: String!) {
  coach {
    id
    studentList(id: $studentListId) {
      id
      name
      autoAssignableStudents {
        id
        kaid
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

CoachAssignments = """query CoachAssignments($studentListId: String!, $assignmentFilters: CoachAssignmentFilters, $orderBy: AssignmentOrder!, $pageSize: Int, $after: ID) {
  coach {
    id
    studentList(id: $studentListId) {
      id
      assignmentsPage(filters: $assignmentFilters, orderBy: $orderBy, after: $after, pageSize: $pageSize) {
        assignments {
          id
          studentKaids
          isDraft
          subjectSlug
          numStudentsCompleted
          assignedDate
          dueDate
          contentDescriptors
          contents {
            id
            title: translatedTitle
            kind
            defaultUrlPath
            __typename
          }
          exerciseConfig {
            itemPickerStrategy
            __typename
          }
          __typename
        }
        pageInfo {
          nextCursor
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

# MUTATIONS

stopCoaching = """mutation stopCoaching($kaids: [ID], $invitationIds: [ID], $coachRequestIds: [ID]) {
  stopCoaching(kaids: $kaids, invitationIds: $invitationIds, coachRequestIds: $coachRequestIds) {
    coach {
      id
      kaid
      __typename
    }
    __typename
  }
}
"""
transferStudents = """mutation transferStudents($fromListIds: [ID], $toListIds: [ID], $kaids: [ID], $invitationIds: [ID], $coachRequestIds: [ID]) {
  transferStudents(fromListIds: $fromListIds, toListIds: $toListIds, kaids: $kaids, invitationIds: $invitationIds, coachRequestIds: $coachRequestIds) {
    coach {
      id
      kaid
      __typename
    }
    __typename
  }
}
"""

updateAutoAssign = """mutation updateAutoAssign($studentListId: String!, $studentKaids: [ID]!, $autoAssign: Boolean!) {
  updateAutoAssign(studentListId: $studentListId, studentKaids: $studentKaids, autoAssign: $autoAssign) {
    coach {
      id
      studentList(id: $studentListId) {
        id
        name
        autoAssignableStudents {
          id
          kaid
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

publishAssignment = """mutation publishAssignment($assignmentId: ID!) {
  updateAssignment(id: $assignmentId, assignment: {isDraft: false}) {
    assignment {
      ...AssignmentInfoFragment
      __typename
    }
    __typename
  }
}

fragment AssignmentInfoFragment on Assignment {
  id
  contents {
    id
    title
    __typename
  }
  studentList {
    id
    name
    __typename
  }
  students {
    id
    kaid
    __typename
  }
  coach {
    id
    kaid
    __typename
  }
  dueDate
  isDraft
  subjectSlug
  __typename
}
"""
