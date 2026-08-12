BLUE='\033[38;5;27m'
GREEN='\033[38;5;43m'
RED='\033[0;31m'
GRAY='\033[0;37m'
RESET='\033[0m'

log_pending() {
  echo "${BLUE}⦿ $1 ${RESET}"
}

log_success() {
  echo "${GREEN}✔ $1 ${RESET}"
}

log_error() {
  echo "${RED}✘ $1 ${RESET}"
}

log_skip() {
  echo "${GRAY}⊝ $1 ${RESET}"
}