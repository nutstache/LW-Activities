import subprocess
import sys

#Storing Mounting and Partition location
print("Enter mount location (Ex /mount_loc/sd1) : ")
mount_dir=input()
print("Enter partition (Ex /dev/sd1) : ")
partition_dir=input()

#Unmount drive
subprocess.getoutput("umount "+mount_dir)

print("Next step will format partition "+ partition_dir+"\n Do you want to continue (y/n)?")
ch=input()
if ch!='y':
	print("Exiting")
	sys.exit()

#Formating drive to clear inodes and get block size
z=subprocess.getoutput("mkfs.ext4 "+partition_dir+" | grep Block")
z=z.split("\n")
z=z[1]
z=z.split()
z=z[1]
z=z.split("=")
block_size=int(z[1])
print("Block size : "+str(block_size))

#Mount drive
subprocess.getstatusoutput("mount "+partition_dir+" "+mount_dir)

#Displaying free Inodes and get free inodes
z=subprocess.getoutput("df -i "+mount_dir)
z=z.split("\n")
z=z[1]
z=z.split()
free_inode=int(z[3])
print("Free Inodes : "+str(free_inode))

#Displaying available blocks and get available blocks
z=subprocess.getoutput("df "+mount_dir)
z=z.split("\n")
z=z[1]
z=z.split()
free_block=int(z[3])
print("Available Blocks : "+str(free_block))

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
free_block=free_block-(int(free_block/free_inode))*(free_inode-1)
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
