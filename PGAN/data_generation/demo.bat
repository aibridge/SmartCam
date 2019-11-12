SET pascal_pose_file_root="./examples/pascalPose.csv"
SET pascal_mask_img_dir="./examples/pascal_mask"
SET origin_img_root="./examples/origin_images"
SET json_file_root="./examples/examples.json"
SET crop_output_path="./examples/outputs/crop_output"
SET experiment_name="pretrained_model"
SET merge_output_path="./examples/outputs/merge_output"
SET overlay_output_path="./examples/outputs/overlay_output"

python crop_pose_and_generate_testing_prior.py --PASCALPoseFileRoot %pascal_pose_file_root% --PASCALMaskImgDir %pascal_mask_img_dir% --n 3 --k 3 --aug 0.25 --origin_img_root %origin_img_root% --json_file_root %json_file_root% --outputDir $crop_output_path
cd refinement_network
python test.py --dataroot ../%crop_output_path% --dataset_mode single --model test --output_nc 1 --name %experiment_name% --which_epoch latest --checkpoints_dir ../examples --results_dir ../examples
cd ..
python merge_parsing_result.py --outputDir %merge_output_path% --parsing_root ./examples/%{experiment_name}%/test_latest/images --origin_img_root %origin_img_root% --json_file_root %json_file_root% --aug 0.25
python overlay.py --origin_img_root %origin_img_root% --parsing_img_root %merge_output_path% --outputDir %overlay_output_path%