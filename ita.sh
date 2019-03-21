clear
echo "\t\t\t\tImage To Audio"
echo
echo "[Initiated]..."
echo
echo "[Optika is going to click the Image. STAND STILL!]"
say "Stand still, optika is going to click the Image."
sleep 2s

# Now Capturing Image.
raspistill -o ITA_output.tiff
echo
echo "[Optika has clicked the image. Now Processing]..."
say "image clicked. now processing..."

# Now Processing.
tesseract ITA_output.tiff stdout > ITA_text.txt
echo
echo "[Image Processed.]"
say "image processed. Playing in one second."
#sleep 5s
cat ITA_text.txt
say -f ITA_text.txt
echo
echo "[Now terminating]"
say "Exiting"
#rm -r ITA_text.txt
