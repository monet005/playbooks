#!/bin/bash

TARGET_DIR=$2
OUT_DIR=${TARGET_DIR}/.ppd_golive
LOGFILE="${OUT_DIR}"/ppd_symlink_logs.txt
MODE=$1
VALID_PRE_HOSTS=("node-1")
VALID_POST_HOSTS=("node-1")

if [[ $# -lt 2 ]]; then
    echo "Usage: $(basename "$0") <pre|post> <target_dir>"
    exit 1
fi

logit () {
    case "$1" in
        fatal) echo "EXITING : $2" | tee -a "$LOGFILE"; exit 1 ;;
        info) echo "INFO : $2" | tee -a "$LOGFILE" ;;
        pass) echo "PASS : $2" | tee -a "$LOGFILE" ;;
    esac
}

if [[ ! -d "$OUT_DIR" ]]; then
    mkdir -p "$OUT_DIR"
fi

case "$MODE" in
    pre)
        if ! echo "${VALID_PRE_HOSTS[@]}" | grep -q "$(uname -n)"; then
            logit fatal "Invalid server to run the script's PRE mode"
        fi
        logit info "Running the script in PRE mode"
        logit info "Target Dir: $TARGET_DIR"
        cd "$TARGET_DIR" || logit fatal "$TARGET_DIR does not exists"
        find . -type l -exec ls -ld {} \; > "${OUT_DIR}"/symlink_capture_pre.txt
        logit info "Symlink configuration has been backed up at ${OUT_DIR}/symlink_capture_pre.txt"
        awk '{print $9,$11}' "${OUT_DIR}"/symlink_capture_pre.txt | sed 's/ /,/g' > "${OUT_DIR}"/symlink_mapping.csv

        # unlink
        while IFS=',' read -r link _; do
            unlink "$link" && logit info "$link symlink has been removed"
        done < "${OUT_DIR}"/symlink_mapping.csv
         ;;

    post) 
        if ! echo "${VALID_POST_HOSTS[@]}" | grep -q "$(uname -n)"; then
            logit fatal "Invalid server to run the script's POST mode"
        fi
        logit info "Running the script in POST mode"
        # relink
        cd "$TARGET_DIR" || logit fatal "$TARGET_DIR does not exists" 
        while IFS=',' read -r link target; do
            ln -s "$target" "$link" && logit pass "$(ls -ld "$link") symlink has been restored"
        done < "${OUT_DIR}"/symlink_mapping.csv
         ;;
    *) logit fatal "Invalid option, exiting...";;
esac

