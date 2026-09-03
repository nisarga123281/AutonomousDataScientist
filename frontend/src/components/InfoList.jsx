
function InfoList({
  title,
  items = [],
}) {

  if (!items.length) {
    return null;
  }

  return (
    <div className="professional-info">

      <div className="info-header">
        <h3>{title}</h3>
        <span>{items.length}</span>
      </div>

      <div className="info-tags">

        {items.map((item, index) => (
          <span key={index}>
            {item}
          </span>
        ))}

      </div>

    </div>
  );
}

export default InfoList;
