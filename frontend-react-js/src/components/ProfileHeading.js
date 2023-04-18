import './ProfileHeading.css';
import EditProfileButton from '../components/EditProfileButton';

export default function ProfileHeading(props) {
    const backgroundImage = 'url("https://assets.ferritinman.com/banners/banner.jpg")';
    const styles = {
      backgroundImage: backgroundImage,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    };

    return (
    <div className='activity_feed_heading profile_heading'>
        <div className='title'>{props.profile.display_name}</div>
        <div className='cruds_count'>{props.profile.cruds_count} Cruds</div>
        <div className="banner" style={styles}>
            <div className="avatar">
                <img src="https://assets.ferritinman.com/avatars/skeletor.jpg" />
            </div>
        </div>
        <div class="info">
            <div class="id">
                <div className="display_name">{props.profile.display_name}</div>
                <div className="handle">@{props.profile.handle}</div>
            </div>
             <EditProfileButton setPopped={props.setPopped} />
        </div>
     </div>  
    );
} 