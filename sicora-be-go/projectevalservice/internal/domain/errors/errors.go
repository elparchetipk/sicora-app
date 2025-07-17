package errors

import "errors"

var (
	// Project errors
	ErrProjectNotFound       = errors.New("project not found")
	ErrProjectAlreadyExists  = errors.New("project already exists")
	ErrProjectInactive       = errors.New("project is inactive")
	ErrProjectDeadlinePassed = errors.New("project deadline has passed")
	ErrInvalidProjectStatus  = errors.New("invalid project status")
	ErrInvalidProjectData    = errors.New("invalid project data")

	// Submission errors
	ErrSubmissionNotFound      = errors.New("submission not found")
	ErrSubmissionAlreadyExists = errors.New("submission already exists for this project")
	ErrSubmissionNotAllowed    = errors.New("submission not allowed for this project")
	ErrInvalidSubmissionStatus = errors.New("invalid submission status")
	ErrInvalidRepositoryURL    = errors.New("invalid repository URL")
	ErrInvalidDeploymentURL    = errors.New("invalid deployment URL")

	// Evaluation errors
	ErrEvaluationNotFound      = errors.New("evaluation not found")
	ErrEvaluationAlreadyExists = errors.New("evaluation already exists for this submission")
	ErrEvaluationNotAllowed    = errors.New("evaluation not allowed for this submission")
	ErrInvalidEvaluationStatus = errors.New("invalid evaluation status")
	ErrInvalidScore            = errors.New("invalid score value")
	ErrEvaluationNotModifiable = errors.New("evaluation cannot be modified")

	// Stakeholder errors
	ErrStakeholderNotFound      = errors.New("stakeholder not found")
	ErrStakeholderAlreadyExists = errors.New("stakeholder already exists for this project")
	ErrStakeholderNotAllowed    = errors.New("stakeholder action not allowed")
	ErrInvalidStakeholderRole   = errors.New("invalid stakeholder role")
	ErrInvalidStakeholderType   = errors.New("invalid stakeholder type")
	ErrInvalidStakeholderStatus = errors.New("invalid stakeholder status")
	ErrStakeholderBlocked       = errors.New("stakeholder is blocked")
	ErrInsufficientPermissions  = errors.New("insufficient permissions")

	// ProjectDocument errors
	ErrDocumentNotFound      = errors.New("document not found")
	ErrDocumentAlreadyExists = errors.New("document already exists")
	ErrDocumentNotAllowed    = errors.New("document action not allowed")
	ErrInvalidDocumentType   = errors.New("invalid document type")
	ErrInvalidDocumentStatus = errors.New("invalid document status")
	ErrDocumentNotModifiable = errors.New("document cannot be modified")
	ErrDocumentTooLarge      = errors.New("document size exceeds limit")
	ErrInvalidFileType       = errors.New("invalid file type")
	ErrDocumentUploadFailed  = errors.New("document upload failed")

	// General errors
	ErrUnauthorized       = errors.New("unauthorized access")
	ErrValidationFailed   = errors.New("validation failed")
	ErrInternalServer     = errors.New("internal server error")
	ErrDatabaseConnection = errors.New("database connection error")
)
