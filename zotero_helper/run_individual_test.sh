s=0
e=1000

while [ "$1" != "" ]; do
    case $1 in
    --s )   shift
            s=$1
            ;;
    --e )   shift
            e=$1
            ;;
    *) break;
    esac;
    shift
done

if [ "$s" -gt "$e" ]
then
    echo "Error: the start must be less than or equal to the end"
    exit 1
fi

message="\nFailed Tests:\n===============\n"
failcount=0
while read -r line; do
    test_num="$((10#${line:4:2}))"
    test_head="${line:4}"
    if [[ $test_num -ge s && $test_num -le e ]]
    then
        output=$(kubectl exec -n guszarzmo -it deploy/tdm -- tala test http://tdm/interact /okteto/zotero_helper/test/interaction_tests_eng.txt -t "${line:4}" 2>&1 </dev/null)
        status=$(echo "$output" | grep "OK")
        if [ -z "$status" ]
        then
            echo "${line:4:2}: Failed."
            message+="${line:4:2}\n-------\n"
            message+=$(echo "$output" | grep -A4 "expected:")
            message+="\n\n\n"
            (( failcount++ ))
        else
            echo "${line:4:2}: Ok."
        fi
    fi

done < <(grep "^--- " zotero_helper/ddds/zotero_helper/zotero_helper/test/interaction_tests_eng.txt)

if [ $failcount -eq 0 ]
then
    message+="No Failed test\n"
fi
echo -e "$message"