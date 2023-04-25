import './ProfileAvatar.css';

export default function ProfileAvatar(props) {
const styles = {
    backgroundImage: `url("https://assets.ferritinman.com/avatars/${props.id}.jpg")`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    };

  return (
    <div 
        className="profile-avatar"
        style={styles}
    ></div>
  );
}