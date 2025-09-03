#!/bin/bash 

echo "Processing..."

end=700

for i in {1..$end}; do
    dir="/path/to/folder/recup_dir.${i}"
    # Checking if dictonary exists
    if [ -d "$dir" ]; then
        python3 "/source/sort_files.py" "$dir"
	# Removing empty 
	if [ && -z "$(ls -A "$dir")" ]; then 
		echo "The dictionary $dir is empty - deleting dict..." 
		rmdir "$dir" 
	fi 
    else 
	    echo "This dictonary is not exist" 
	fi 
done

echo "Closing..."
