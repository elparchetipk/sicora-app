# SICORA Frontend - Automated Commit Strategy

## 🎯 **Philosophy: Zero-Configuration Automation**

Everything is automated to follow best practices without manual intervention. Developers focus on coding, tools handle the rest.

## 🚀 **Automated Commit Workflow**

### **1. Interactive Commit (Recommended)**

```bash
pnpm run commit
```

This launches an interactive wizard that:

- ✅ **Guides you through** conventional commit format
- ✅ **Suggests appropriate scopes** based on changed files
- ✅ **Validates message format** before committing
- ✅ **Shows examples** for each commit type
- ✅ **Handles breaking changes** automatically

### **2. Manual Commit (Validated)**

```bash
git commit -m "feat(atoms): add TouchButton with mobile optimization"
```

Even manual commits are automatically:

- ✅ **Validated** for conventional format
- ✅ **Linted and formatted** via pre-commit hooks
- ✅ **Type-checked** for TypeScript errors
- ✅ **Rejected** if validation fails

### **3. Signed Commits (Optional)**

```bash
pnpm run commit:signed
```

For teams requiring signed commits (recommended for production).

## 📋 **Conventional Commit Format**

### **Structure**

```
type(scope): description

[optional body]

[optional footer(s)]
```

### **Examples by Component Type**

#### **Atomic Design Components:**

```bash
feat(atoms): add TouchButton component with SENA colors
fix(molecules): resolve UserCard layout issue on mobile
style(organisms): improve MobileAttendanceList spacing
test(templates): add AdaptiveLayout responsive tests
```

#### **Feature Development:**

```bash
feat(pages): implement LoginPage with mobile-first design
feat(hooks): add useViewport for responsive behavior
feat(services): create attendanceService API client
```

#### **Bug Fixes:**

```bash
fix(mobile): resolve touch target size on small screens
fix(pwa): correct service worker caching strategy
fix(sena): ensure color compliance in button variants
```

#### **Documentation & Maintenance:**

```bash
docs(mobile): update mobile-first strategy guide
chore(deps): update React to 18.2.1
ci(docker): optimize production image size
```

## 🔧 **Pre-commit Automation**

Every commit automatically triggers:

### **1. Code Quality (< 30 seconds)**

```bash
# ESLint with auto-fix
eslint src --ext ts,tsx --fix

# Prettier formatting
prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,md}"

# TypeScript type checking
tsc --noEmit
```

### **2. Validation**

```bash
# Commit message validation
commitlint --edit $COMMIT_MSG_FILE

# Staged files only (optimized)
lint-staged
```

## 🎨 **Scope-Based Organization**

### **Component Scopes (Atomic Design)**

- `atoms`: TouchButton, TouchInput, StatusBadge, LoadingSpinner
- `molecules`: LoginForm, UserCard, AttendanceRow, SearchInput
- `organisms`: MobileAttendanceList, AdaptiveNavigation, DashboardHeader
- `templates`: AdaptiveLayout, AuthLayout, EmptyStateLayout

### **Feature Scopes**

- `pages`: Login, Dashboard, Attendance, Profile pages
- `features`: Attendance-specific, Reports-specific components
- `hooks`: useViewport, useAuth, useAttendance
- `services`: API clients, external integrations
- `utils`: Helper functions, formatters, validators

### **Technical Scopes**

- `config`: Vite, TypeScript, Tailwind configuration
- `docker`: Containerization and deployment
- `ci`: GitHub Actions, automation
- `deps`: Dependency management
- `security`: Security-related changes

### **SENA-Specific Scopes**

- `sena`: Identity compliance, colors, typography
- `mobile`: Mobile-first optimizations
- `pwa`: Progressive Web App features
- `a11y`: Accessibility improvements

## 🔄 **Automated Branch Strategy**

### **Branch Naming Convention**

```bash
# Feature branches
feature/atoms-touch-button
feature/mobile-attendance-list
feature/sena-color-compliance

# Bug fix branches
fix/mobile-touch-targets
fix/pwa-caching-strategy

# Documentation branches
docs/mobile-first-update
docs/atomic-design-guide
```

### **Automated Branch Actions**

- ✅ **Pull Request**: Auto-triggers full CI/CD pipeline
- ✅ **Develop Branch**: Auto-deploys to staging
- ✅ **Main Branch**: Auto-deploys to production
- ✅ **Feature Branches**: Auto-runs quality checks

## 📊 **Quality Metrics & Reporting**

### **Automated Quality Gates**

Every commit must pass:

- ✅ **TypeScript**: Zero compilation errors
- ✅ **ESLint**: Zero linting errors (after auto-fix)
- ✅ **Prettier**: Consistent formatting
- ✅ **Tests**: All existing tests pass
- ✅ **Convention**: Valid conventional commit format

### **CI/CD Quality Reports**

- 📊 **Test Coverage**: Tracked and reported
- 📊 **Bundle Size**: Monitored for regressions
- 📊 **Performance**: Lighthouse scores on every PR
- 📊 **Security**: Dependency vulnerability scanning
- 📊 **Accessibility**: Automated a11y testing

## 🚨 **Error Handling & Recovery**

### **Common Issues & Auto-Resolution**

#### **Formatting Issues**

```bash
# Automatically fixed by pre-commit hooks
Error: Code not formatted
Solution: Prettier runs automatically ✅
```

#### **Linting Issues**

```bash
# Most issues auto-fixed, others reported clearly
Error: ESLint violations
Solution: Auto-fix runs, manual fixes needed for remaining ✅
```

#### **Type Errors**

```bash
# Clear TypeScript errors with file locations
Error: TypeScript compilation failed
Solution: Fix types before commit is allowed ❌
```

#### **Invalid Commit Messages**

```bash
# Interactive correction with examples
Error: Commit message format invalid
Solution: Use `pnpm run commit` for guided format ✅
```

### **Recovery Commands**

```bash
# Reset and try again
git reset --soft HEAD~1
pnpm run commit

# Force format all files
pnpm run format

# Fix all auto-fixable linting issues
pnpm run lint:fix

# Type check entire project
pnpm run type-check
```

## 🔍 **Monitoring & Analytics**

### **Development Metrics (Weekly)**

- 📈 **Commit frequency** and consistency
- 📈 **Convention compliance** percentage
- 📈 **Pre-commit hook** success rate
- 📈 **CI/CD pipeline** success rate

### **Code Quality Trends**

- 📊 **Test coverage** evolution
- 📊 **Bundle size** growth tracking
- 📊 **Performance scores** over time
- 📊 **Dependency freshness** monitoring

## 🎓 **Learning & Best Practices**

### **For New Developers**

1. **Always use** `pnpm run commit` initially
2. **Learn from examples** in commit history
3. **Check CI/CD feedback** for improvements
4. **Follow scope conventions** consistently

### **Team Guidelines**

- ✅ **Prefer small, focused commits** over large ones
- ✅ **Use descriptive commit messages** with context
- ✅ **Test locally** before pushing (automated)
- ✅ **Keep commits atomic** (one change, one commit)

### **SENA-Specific Guidelines**

- 🎨 **Always mention SENA compliance** in color/design commits
- 📱 **Reference mobile-first** in responsive commits
- ♿ **Include accessibility impact** in a11y commits
- 🔒 **Document security considerations** in security commits

---

## 🎯 **Summary: Zero-Configuration Development**

The entire commit process is designed to be:

- **🤖 Automated**: Tools handle formatting, linting, validation
- **🎯 Guided**: Interactive wizards prevent mistakes
- **📊 Monitored**: Quality metrics tracked automatically
- **🔄 Consistent**: Same process for all team members
- **📱 Mobile-First**: Optimized for SICORA's use cases
- **🎨 SENA-Compliant**: Enforces identity guidelines

**Just code and commit - everything else is automated!**
