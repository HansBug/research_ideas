open Reproduction/DriverLicense

pred ExampleInstance {
  #Applicant = 1
  #DrivingLicense = 1
  #TestRecord = 3
}

assert SingleCurrentLicense {
  all a : Applicant | lone a.currentLicense
}

assert TestRecordBackReference {
  all t : TestRecord | t in t.applicant.testRecords
}

assert EveryApplicantHasALicense {
  all a : Applicant | one a.currentLicense
}

run ExampleInstance for 12 Int, exactly 1 Applicant, exactly 1 DrivingLicense, exactly 3 TestRecord
check SingleCurrentLicense for 12 Int, exactly 1 Applicant, exactly 1 DrivingLicense, exactly 3 TestRecord
check TestRecordBackReference for 12 Int, exactly 1 Applicant, exactly 1 DrivingLicense, exactly 3 TestRecord
check EveryApplicantHasALicense for 12 Int, exactly 1 Applicant, exactly 0 DrivingLicense, exactly 0 TestRecord
