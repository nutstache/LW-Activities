import subprocess

#Storing Mounting and Partition location
print("Enter mount location (Ex /mount_loc/sdb1) : ")
mount_dir=input()
print("Enter partition (Ex /dev/sdb1) : ")
partition_dir=input()

#Unmount drive
subprocess.getoutput("umount "+mount_dir)


#Formating drive to clear inodes and asking user to store the value
z=subprocess.getoutput("mkfs.ext4 "+partition_dir+" | grep Block")
print(z)
print("Enter block size : ")
block_size=int(input())

#Mount drive
subprocess.getstatusoutput("mount "+partition_dir+" "+mount_dir)

#Displaying free Inodes and storing value form user
z=subprocess.getoutput("df -i "+mount_dir)
print(z)
print("Enter number of free Inodes : ")
free_inode=int(input())

#Displaying available blocks and storing value from user
z=subprocess.getoutput("df "+mount_dir)
print(z)
print("Enter number of available blocks : ")
free_block=int(input())

#Size of each file which will be created
print("File Size ="+str(int(free_block*block_size/free_inode)))

#Creating files to fill drive
for i in range(free_inode-1):

	subprocess.getstatusoutput("touch "+mount_dir+"/text{}.txt".format(i))
	
	#Writing data to files
	file=open(mount_dir+"/text{}.txt".format(i),mode="w")
	for j in range(int(free_block/free_inode)*block_size):
		file.write("?")
	file.close()


#Creating last file to cover remaining blocks
free_block=free_block-(int(free_block/free_inode)-1)*free_block
subprocess.getoutput("touch "+mount_dir+"/last_block.txt")
file=open(mount_dir+"/last_block.txt",mode="w")
for i in range(free_block*block_size):
	file.write("?")
file.close()


print("\n\n \t\tFinal State \n")
print(subprocess.getoutput("df -i "+mount_dir)+"\n")
print(subprocess.getoutput("df "+mount_dir)+"\n")


print("Do you want to remove new files?(y/n)")
ch=input()
if ch=='y':
	subprocess.getoutput("rm -rf "+mount_dir+"/*")
